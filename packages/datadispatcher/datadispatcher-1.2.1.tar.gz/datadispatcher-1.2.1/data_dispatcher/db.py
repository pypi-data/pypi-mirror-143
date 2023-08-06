import json, time, io
from datetime import datetime, timedelta, timezone
from metacat.auth import BaseDBUser as DBUser

def cursor_iterator(c):
    t = c.fetchone()
    while t is not None:
        yield t
        t = c.fetchone()


def json_literal(v):
    if isinstance(v, str):       v = '"%s"' % (v,)
    elif isinstance(v, bool):    v = "true" if v else "false"
    elif v is None:              v = "null"
    else:   v = str(v)
    return v

class DBObject(object):
    
    @classmethod
    def from_tuple(cls, db, dbtup):
        h = cls(db, *dbtup)
        return h
    
    @classmethod
    def columns(cls, table_name=None, as_text=True, exclude=[]):
        if isinstance(exclude, str):
            exclude = [exclude]
        clist = [c for c in cls.Columns if c not in exclude]
        if table_name:
            clist = [table_name+"."+cn for cn in clist]
        if as_text:
            return ",".join(clist)
        else:
            return clist
    
    @classmethod
    def pk_columns(cls, table_name=None, as_text=True, exclude=[]):
        if isinstance(exclude, str):
            exclude = [exclude]
        clist = [c for c in cls.PK if c not in exclude]
        if table_name:
            clist = [table_name+"."+cn for cn in clist]
        if as_text:
            return ",".join(clist)
        else:
            return clist
    
    @classmethod
    def get(cls, db, *pk_vals):
        pk_cols_values = [f"{c} = %s" for c in cls.PK]
        where = " and ".join(pk_cols_values)
        cols = ",".join(cls.Columns)
        c = db.cursor()
        c.execute(f"select {cols} from {cls.Table} where {where}", pk_vals)
        tup = c.fetchone()
        if tup is None: return None
        else:   return cls.from_tuple(db, tup)

    def _delete(self, cursor=None, do_commit=True, **pk_values):
        cursor = cursor or self.DB.cursor()
        where_clause = " and ".join(f"{column} = '{value}'" for column, value in pk_values.items())
        try:
            cursor.execute(f"""
                delete from {self.Table} where {where_clause}
            """)
            if do_commit:
                cursor.execute("commit")
        except:
            cursor.execute("rollback")
            raise
    
    @classmethod
    def list(db, cls):
        columns = cls.columns(as_text=True)
        table = cls.Table
        c = db.cursor()
        c.execute(f"select {columns} from {table}")
        return (cls.from_tuple(db, tup) for tup in cursor_iterator(c))
    
    def delete(self, cursor=None, do_commit=True, **pk_values):
        return self._delete(cursor=None, do_commit=True, **pk_values)
    
class DBManyToMany(object):
    
    def __init__(self, db, table, src_fk_values, dst_fk_columns, payload_columns, dst_class):
        self.DB = db
        self.Table = table
        self.SrcFKColumns, self.SrcFKValues = zip(*list(src_fk_values.items()))
        self.DstFKColumns = dst_fk_columns
        self.DstClass = dst_class
        self.DstTable = dst_class.Table
        self.DstPKColumns = self.DstTable.PK

    def add(self, dst_pk_values, payload, cursor=None, do_commit=True):
        assert len(dst_pk_values) == len(self.DstFKColumns)
        
        payload_cols_vals = list(payload.items())
        payload_cols, payload_vals = zip(*payload_cols_vals)
        
        fk_cols = ",".join(self.SrcFKColumns + self.DstFKColumns)
        cols = ",".join(self.SrcFKColumns + self.DstFKColumns + payload_cols)
        vals = ",".join([f"'{v}'" for v in self.SrcFKValues + dst_pk_values + payload_vals])
        
        if cursor is None: cursor = self.DB.cursor()
        try:
            cursor.execute(f"""
                insert into {self.Table}({cols}) values({vals})
                    on conflict({fk_cols}) do nothing
            """)
            if do_commit:
                cursor.execute("commit")
        except:
            cursor.execute(rollback)
            raise
        return self

    def list(self, cursor=None):
        out_columns = ",".join(f"{self.DstTable}.{c}" for c in self.DstClass.Columns)
        join_column_pairs = [
            (f"{self.Table}.{dst_fk}", f"{self.DstTable}.{dst_pk}") 
            for src_fk, dst_pk in zip(self.DstFKColumns, self.DstPKColumns)
        ]
        join_condition = " and ".join(f"{fk} = {pk}" for fk, pk in join_column_pairs)
        if cursor is None: cursor = self.DB.cursor()
        cursor.execute(f"""
            select {out_columns}
                from {self.DstTable}, {self.Table}
                where {join_condition}
        """)
        return (self.DstClass.from_tuple(self.DB, tup) for tup in fetch_generator(cursor))
        
    def __iter__(self):
        return self.list()

class DBOneToMany(object):
    
    def __init__(self, db, table, src_pk_values, dst_fk_columns, dst_class):
        self.DB = db
        self.Table = table
        self.SrcPKColumns, self.SrcPKValues = zip(*list(src_pk_values.items()))
        self.DstClass = dst_class
        self.DstTable = dst_class.Table
        self.DstFKColumns = dst_fk_columns

    def list(self, cursor=None):
        out_columns = ",".join(f"{self.DstTable}.{c}" for c in self.DstClass.Columns)
        join_column_pairs = [
            (f"{self.Table}.{dst_pk}", f"{self.DstTable}.{dst_fk}") 
            for src_pk, dst_fk in zip(self.SrcPKColumns, self.DstFKColumns)
        ]
        join_condition = " and ".join(f"{pk} = {fk}" for pk, fk in join_column_pairs)
        if cursor is None: cursor = self.DB.cursor()
        cursor.execute(f"""
            select {out_columns}
                from {self.DstTable}, {self.Table}
                where {join_condition}
        """)
        return (self.DstClass.from_tuple(self.DB, tup) for tup in fetch_generator(cursor))
        
    def __iter__(self):
        return self.list()

class HasLogRecord(object):

    def __init__(self, log_table, id_column):
        self.LogTable = log_table
        self.IDColumn = id_column
    
    class DBLogRecord(object):
    
        def __init__(self, type, t, message):
            self.Type = type
            self.T = t
            self.Message = message

    def id(self):
        raise NotImplementedError()

    def add_log(self, type, message):
        c = self.DB.cursor()
        c.execute(f"""
            begin;
            
            insert into {self.LogTable}({self.IDColumn}, type, message)
            values(%s, %s, %s);

            commit
        """, (self.ID, type, message))

    def log(self, type=None, since=None, reversed=False):
        my_id = self.id()
        wheres = [f"column={my_id}"]
        if isinstance(since, (float, int)):
            since = datetime.utcfromtimestamp(since).replace(tzinfo=timezone.utc)
            wheres.append(f"t >= {since}")
        if type is not None:
            wheres.append(f"type = '{type}'")
        wheres = "" if not wheres else " and " + " and ".join(wheres)
        desc = "desc" if reversed else ""
        sql = f"""
            select type, t, message from {self.LogTable}
                {wheres}
                order by t {desc}
        """
        c = self.DB.cursor()
        c.execute(sql)
        return (self.DBLogRecord(type, t, message) for type, t, message in cursor_iterator())
        

class DBProject(DBObject, HasLogRecord):
    
    InitialState = "active"
    
    Columns = "id,owner,created_timestamp,state,retry_count,attributes".split(",")
    Table = "projects"
    PK = ["id"]
    
    def __init__(self, db, id, owner=None, created_timestamp=None, state=None, retry_count=0, attributes={}):
        HasLogRecord.__init__(self, "project_log", "project_id")
        self.DB = db
        self.ID = id
        self.Owner = owner
        self.State = state
        self.CreatedTimestamp = created_timestamp               # datetime
        self.RetryCount = retry_count
        self.Attributes = attributes.copy()
        self.Handles = None
        self.HandleCounts = None
        
    def id(self):
        return str(self.ID)
        
    def as_jsonable(self, with_handles=False, with_replicas=False):
        #print("Project.as_jsonable: with_handles:", with_handles, "   with_replicas:", with_replicas)
        out = dict(
            project_id = self.ID,
            owner = self.Owner,
            state = self.State,
            retry_count = self.RetryCount,
            attributes = self.Attributes,
            created_timestamp = self.CreatedTimestamp.timestamp(),
            active = self.is_active()
        )
        if with_handles:
            out["file_handles"] = [h.as_jsonable(with_replicas=with_replicas) for h in self.handles()]
            #print("Project.as_jsonable: handles:", out["file_handles"])
        return out

    def attributes_as_json(self):
        return json.dumps(self.Attributes, indent=4)
        
    @staticmethod
    def create(db, owner, retry_count=None, attributes={}):
        if isinstance(owner, DBUser):
            owner = owner.Username
        c = db.cursor()
        try:
            c.execute("begin")
            c.execute("""
                insert into projects(owner, state, retry_count, attributes)
                    values(%s, %s, %s, %s)
                    returning id
            """, (owner, DBProject.InitialState, retry_count, json.dumps(attributes)))
            id = c.fetchone()[0]
            db.commit()
        except:
            db.rollback()
            raise
            
        return DBProject.get(db, id)

    @staticmethod
    def list(db, owner=None, state=None, not_state=None, attributes=None, with_handle_counts=False):
        wheres = ["true"]
        if owner: wheres.append(f"p.owner='{owner}'")
        if state: wheres.append(f"p.state='{state}'")
        if not_state: wheres.append(f"p.state!='{not_state}'")
        if attributes is not None:
            for name, value in attributes.items():
                wheres.append("p.attributes @> '{\"%s\": %s}'::jsonb" % (name, json_literal(value)))
        wheres = " and ".join(wheres)
        c = db.cursor()
        table = DBProject.Table
        columns = DBProject.columns("p", as_text=True)
        if with_handle_counts:
            h_table = DBFileHandle.Table
            c.execute(f"""
                select {columns}, h.state, count(*)
                    from {table} p, {h_table} h
                    where {wheres}
                        and p.id = h.project_id
                    group by {columns}, h.state
                    order by p.id
            """)
            p = None
            for tup in cursor_iterator(c):
                #print(tup)
                p_tuple, h_state, count = tup[:len(DBProject.Columns)], tup[-2], tup[-1]
                p1 = DBProject.from_tuple(db, p_tuple)
                if p is None or p.ID != p1.ID:
                    if p is not None:
                        yield p
                    p = p1
                    p.HandleCounts = {state:0 for state in DBFileHandle.States}
                p.HandleCounts[h_state] = count
            if p is not None:
                yield p
        else:
            c.execute(f"""
                select {columns}
                    from {table} p
                    where {wheres}
            """)
            for tup in cursor_iterator(c):
                yield DBProject.from_tuple(db, tup)
        
    def save(self):
        c = self.DB.cursor()
        try:
            c.execute("begin")
            c.execute("""
                update projects set state=%s
                    where id=%s
            """, (self.State, self.ID))
            self.DB.commit()
        except:
            self.DB.rollback()
            raise
        
    def handles(self, with_replicas=True):
        if self.Handles is None:
            self.Handles = list(DBFileHandle.list(self.DB, project_id=self.ID, with_replicas=with_replicas))
        return self.Handles
        
    def handle(self, namespace=None, name=None):
        return DBFileHandle.lookup(self.DB, project_id=self.ID, namespace=namespace, name=name)
            
    def add_files(self, files_descs):
        # files_descs is list of disctionaries: [{"namespace":..., "name":...}, ...]
        files_descs = list(files_descs)     # make sure it's not a generator
        DBFile.create_many(self.DB, files_descs)
        DBFileHandle.create_many(self.DB, self.ID, files_descs)
        
    def files(self):
        return DBFile.list(self.DB, self.ID)
        
    def reserve_next_file(self, worker_id):
        handle = DBFileHandle.reserve_next_available(self.DB, self.ID, worker_id)
        if handle is not None:
            did = handle.did()
            self.add_log("workflow", f"file {did} reserved for {worker_id}")
        return handle

    def is_active(self):
        lst = DBFileHandle.list(self.DB, project_id=self.ID, state=["ready", "reserved"])
        for h in lst:       # lst may be a generator
            return True
        else:
            return False
            
    def file_state_counts(self):
        counts = {}
        for h in DBFileHandle.list(self.DB, project_id=self.ID):
            s = h.State
            counts[s] = counts.get(s, 0) + 1
        return out
        
class DBFile(DBObject):
    
    Columns = ["namespace", "name"]
    PK = ["namespace", "name"]
    Table = "files"
    
    def __init__(self, db, namespace, name):
        self.DB = db
        self.Namespace = namespace
        self.Name = name
        self.Replicas = None	# {rse -> DBReplica}
    
    def id(self):
        return f"{self.Namespace}:{self.Name}"

    def did(self):
        return f"{self.Namespace}:{self.Name}"

    def as_jsonable(self, with_replicas=False):
        out = dict(
            namespace   = self.Namespace,
            name        = self.Name,
        )
        if with_replicas:
            out["replicas"] = {rse: r.as_jsonable() for rse, r in self.replicas().items()}
        return out
        
    def replicas(self):
        if self.Replicas is None:
            self.Replicas = {r.RSE: r for r in DBReplica.list(self.DB, self.Namespace, self.Name)}
        return self.Replicas

    def create_replica(self, rse, path, url, preference=0, available=False):
        DBReplica.create(self.DB, self.Namespace, self.Name, rse, path, url, preference=preference, available=available)
        self.Replicas = None	# force re-load from the DB
        
    def get_replica(self, rse):
        return self.replicas().get(rse)
        
    @staticmethod
    def create(db, namespace, name, error_if_exists=False):
        c = self.DB.cursor()
        try:
            c.execute("begin")
            conflict = "on conflict (namespace, name) do nothing" if not error_if_exists else ""
            c.execute(f"insert into files(namespace, name) values(%s, %s) {conflict}; commit" % (namespace, name))
            return DBFile.get(db, namespace, name)
        except:
            c.execute("rollback")
            raise

    @staticmethod
    def create_many(db, descs):
        #
        # descs: [{"namespace":..., "name":..., ...}]
        #
        csv = [f"%s\t%s" % (item["namespace"], item["name"]) for item in descs]
        data = io.StringIO("\n".join(csv))
        table = DBFile.Table
        c = db.cursor()
        try:
            t = int(time.time()*1000)
            temp_table = f"files_temp_{t}"
            c.execute("begin")
            c.execute(f"create temp table {temp_table} (namespace text, name text)")
            c.copy_from(data, temp_table)
            c.execute(f"""
                insert into {table}(namespace, name)
                    select namespace, name from {temp_table}
                    on conflict(namespace, name) do nothing;
                drop table {temp_table};
                commit
                """)
        except Exception as e:
            c.execute("rollback")
            raise
            
    @staticmethod
    def list(db, project=None):
        project_id = project.ID if isinstance(project, DBProject) else project
        c = db.cursor()
        table = DBFile.Table
        columns = DBFile.columns(as_text=True)
        files_columns = DBFile.columns(table, as_text=True)
        project_where = f" id = {project_id} " if project is not None else " true "
        c.execute(f"""
            select {columns}
                from {table}, projects
                where {project_where}
        """)
        return (DBFile.from_tuple(db, tup) for tup in cursor_iterator(c))

    @staticmethod
    def delete_many(db, specs):
        csv = [f"{namespace}:{name}"  for namespace, name in specs]
        data = io.StringIO("\n".join(csv))
        
        c = db.cursor()
        try:
            t = int(time.time()*1000)
            temp_table = f"files_temp_{t}"
            c.execute("begin")
            c.execute(f"creare temp table {temp_table} (spec text)")
            c.copy_from(data, temp_table)
            c.execute(f"""
                delete from {self.Table} 
                    where namespace || ':' || name in 
                        (select * from {temp_table});
                    on conflict (namespace, name) do nothing;       -- in case some other projects still use it
                drop table {temp_table};
                commit
                """)
        except Exception as e:
            c.execute("rollback")
            raise
    
class DBReplica(DBObject):
    Table = "replicas"
    Columns = ["namespace", "name", "rse", "path", "url", "preference", "available"]
    PK = ["namespace", "name", "rse"]
    
    def __init__(self, db, namespace, name, rse, path, url, preference=0, available=False):
        self.DB = db
        self.Namespace = namespace
        self.Name = name
        self.RSE = rse
        self.URL = url
        self.Path = path
        self.Preference = preference
        self.Available = available
        
    def did(self):
        return f"{self.Namespace}:{self.Name}"

    @staticmethod
    def list(db, namespace=None, name=None):
        c = db.cursor()
        wheres = " true "
        if namespace:   wheres += f" and namespace='{namespace}'"
        if name:        wheres += f" and name='{name}'"
        columns = DBReplica.columns(as_text=True)
        table = DBReplica.Table
        c.execute(f"""
            select {columns} from {table}
            where {wheres}
        """)
        return (DBReplica.from_tuple(db, tup) for tup in cursor_iterator(c))
        
    def as_jsonable(self):
        return dict(name=self.Name, namespace=self.Namespace, path=self.Path, 
            url=self.URL, rse=self.RSE,
            preference=self.Preference, available=self.Available)

    @staticmethod
    def create(db, namespace, name, rse, path, url, preference=0, available=False, error_if_exists=False):
        c = db.cursor()
        table = DBReplica.Table
        try:
            c.execute("begin")
            c.execute(f"""
                insert into {table}(namespace, name, rse, path, url, preference, available)
                    values(%s, %s, %s, %s, %s, %s, %s)
                    on conflict(namespace, name, rse)
                        do update set path=%s, url=%s, preference=%s, available=%s;
                commit
            """, (namespace, name, rse, path, url, preference, available,
                    path, url, preference, available)
            )
        except:
            c.execute("rollback")
            raise
            
        return DBReplica.get(db, namespace, name, rse)

    def save(self):
        table = self.Table
        c = self.DB.cursor()
        try:
            c.execute(f"""
                begin;
                update {table}
                     set path=%s, url=%s, preference=%s, available=%s
                     where namespace=%s and name=%s and rse=%s;
                commit
            """, (self.Path, self.URL, self.Preference, self.Available, self.Namespace, self.Name, self.RSE))
        except:
            c.execute("rollback")
            raise
        return self

    #
    # bulk operations
    #
    @staticmethod
    def remove_bulk(db, rse, dids):
        if not dids:    return
        c = db.cursor()
        table = DBReplica.Table
        try:
            c.execute(f"""
                begin;
                delete from {table}
                    where rse=%s and namespace || ':' || name = any(%s);
                commit
            """, (rse, dids))
        except:
            c.execute("rollback")
            raise

    @staticmethod
    def create_bulk(db, rse, preference, replicas):
        # replicas: {(namespace, name) -> {"path":.., "url":..}}
        # do not touch availability, update if exists

        csv = ['%s\t%s\t%s\t%s\t%s\t%s' % (namespace, name, rse, info["path"], info["url"], preference) 
            for (namespace, name), info in replicas.items()]
        #print("DBReplica.create_bulk: csv:", csv)
        data = io.StringIO("\n".join(csv))
        table = DBReplica.Table
        columns = DBReplica.columns(as_text=True)
        c = db.cursor()
        try:
            t = int(time.time()*1000)
            temp_table = f"file_replicas_temp_{t}"
            c.execute("begin")
            c.execute(f"create temp table {temp_table} (ns text, n text, r text, p text, u text, pr int)")
            c.copy_from(data, temp_table)
            c.execute(f"""
                insert into {table}({columns}) 
                    select t.ns, t.n, t.r, t.p, t.u, t.pr, false from {temp_table} t
                    on conflict (namespace, name, rse)
                        do nothing;
                drop table {temp_table};
                commit
                """)
        except Exception as e:
            c.execute("rollback")
            raise

    @staticmethod
    def update_availability_bulk(db, available, rse, dids):
        # dids is list of dids: ["namespace:name", ...]
        if not dids:    return
        table = DBReplica.Table
        val = "true" if available else "false"
        c = db.cursor()
        c.execute("begin")
        try:
            sql = f"""
                update {table}
                    set available=%s
                    where namespace || ':' || name = any(%s)
                        and rse = %s;
                commit
            """
            c.execute(sql, (val, dids, rse))
        except:
            c.execute("rollback")
            raise

class DBFileHandle(DBObject):

    Columns = ["project_id", "namespace", "name", "state", "worker_id", "attempts", "attributes"]
    PK = ["project_id", "namespace", "name"]
    Table = "file_handles"
    
    InitialState = ReadyState = "ready"
    ReservedState = "reserved"
    States = ["ready", "reserved", "done", "failed"]
    
    def __init__(self, db, project_id, namespace, name, state=None, worker_id=None, attempts=0, attributes={}):
        HasLogRecord.__init__(self, "file_handle_log", "file_handle_id")
        self.DB = db
        self.ProjectID = project_id
        self.Namespace = namespace
        self.Name = name
        self.State = state or self.InitialState
        self.WorkerID = worker_id
        self.Attempts = attempts
        self.Attributes = attributes.copy()
        self.File = None
        self.Replicas = None
        
    def id(self):
        return f"{self.ProjectID}:{self.Namespace}:{self.Name}"
        
    @staticmethod
    def unpack_id(id):
        project_id, namespace, name = id.split(":", 2)
        return int(project_id), namespace, name

    def did(self):
        return f"{self.Namespace}:{self.Name}"

    def get_file(self):
        if self.File is None:
            self.File = DBFile.get(self.DB, self.Namespace, self.Name)
        return self.File
        
    def replicas(self):
        if self.Replicas is None:
            self.Replicas = self.get_file().replicas()
        return self.Replicas
        
    def sorted_replicas(self):
        replicas = self.replicas().values()
        return sorted(replicas,
            key = lambda r: (
                0 if r.Available else 1,
                -r.Preference
            )
        )

    def as_jsonable(self, with_replicas=False):
        out = dict(
            project_id = self.ProjectID,
            namespace = self.Namespace,
            name = self.Name,
            state = self.State,
            worker_id = self.WorkerID,
            attempts = self.Attempts,
            attributes = self.Attributes
        )
        if with_replicas:
            out["replicas"] = {rse:r.as_jsonable() for rse, r in self.replicas().items()}
        return out
        
    def attributes_as_json(self):
        return json.dumps(self.Attributes, indent=4)
        
    @staticmethod
    def from_tuple(db, dbtup):
        #print("Handle.from_tuple: tuple:", dbtup)
        project_id, namespace, name, state, worker_id, attempts, attributes = dbtup
        h = DBFileHandle(db, project_id, namespace, name, state=state, worker_id=worker_id, attempts=attempts, attributes=attributes)
        return h
        
    @staticmethod
    def create(db, project_id, namespace, name, attributes={}):
        c = db.cursor()
        try:
            c.execute("begin")
            c.execute("""
                insert into file_handles(project_id, namespace, name, state, attempts, attributes)
                    values(%s, %s, %s, %s, 0, %s)
            """, (project_id, namespace, name, DBFileHandle.InitialState, json.dumps(attributes)))
            id = c.fetchone()[0]
            db.commit()
        except:
            c.execute("rollback")
            raise
        return DBFileHandle.get(db, project_id, namespace, name)
    
    @staticmethod
    def create_many(db, project_id, files):
        #
        # files: [ {"name":"...", "namespace":"...", "attributes":{}}]
        #
        files_csv = []
        parents_csv = []
        null = r"\N"
        for info in files:
            namespace = info["namespace"]
            name = info["name"]
            attributes = info.get("attributes", {})
            files_csv.append("%s\t%s\t%s\t%s\t%s" % (project_id, namespace, name, DBFileHandle.InitialState, json.dumps(attributes)))
        
        c = db.cursor()
        try:
            c.execute("begin")
            c.copy_from(io.StringIO("\n".join(files_csv)), "file_handles", 
                    columns = ["project_id", "namespace", "name", "state", "attributes"])
            c.execute("commit")
        except Exception as e:
            c.execute("rollback")
            raise
    
    @staticmethod
    def list(db, project_id=None, state=None, namespace=None, not_state=None, with_replicas=False):
        wheres = ["true"]
        if project_id: wheres.append(f"h.project_id={project_id}")
        if state:  
            if isinstance(state, (list, tuple)):
                wheres.append("h.state in (%s)" % ",".join(f"'{s}'" for s in state))
            else:
                wheres.append(f"h.state='{state}'")
        if not_state:       wheres.append(f"h.state!='{not_state}'")
        if namespace:       wheres.append(f"h.namespace='{namespace}'")
        wheres = " and ".join(wheres)
        c = db.cursor()
        h_columns = DBFileHandle.columns("h", as_text=True)
        r_columns = DBReplica.columns("r", as_text=True)
        h_n_columns = len(DBFileHandle.Columns)
        if with_replicas:
            sql = f"""
                select {h_columns}, {r_columns}
                    from file_handles h
                        left outer join replicas r on (r.name = h.name and r.namespace = h.namespace)
                        where {wheres}
                        order by h.namespace, h.name
            """
            #print("DBFileHandle.list: sql:", sql)
            c.execute(sql)
            h = None
            for tup in cursor_iterator(c):
                #print("DBFileHandle.list:", tup)
                h_tuple, r_tuple = tup[:h_n_columns], tup[h_n_columns:]
                if h is None:
                    h = DBFileHandle.from_tuple(db, h_tuple)
                h1 = DBFileHandle.from_tuple(db, h_tuple)
                if h1.Namespace != h.Namespace or h1.Name != h.Name:
                    if h:   
                        #print("    yield:", h)
                        yield h
                    h = h1
                if r_tuple[0] is not None:
                    r = DBReplica.from_tuple(db, r_tuple)
                    h.Replicas = h.Replicas or {}
                    h.Replicas[r.RSE] = r
            if h is not None:
                #print("    yield:", h)
                yield h

        else:
            sql = f"""
                select {h_columns}
                    from file_handles h
                        where {wheres}
            """
            c.execute(sql)
            yield from (DBFileHandle.from_tuple(db, tup) for tup in cursor_iterator(c))
                    
    def save(self):
        c = self.DB.cursor()
        try:
            c.execute("begin")
            c.execute("""
                update file_handles set state=%s, worker_id=%s, attempts=%s, attributes=%s
                    where project_id=%s and namespace=%s and name=%s
            """, (self.State, self.WorkerID, self.Attempts, json.dumps(self.Attributes), 
                    self.ProjectID, self.Namespace, self.Name
                )            
            )
            #print("DBFileHandle.save: attempts:", self.Attempts)
            self.DB.commit()
        except Exception as e:
            c.execute("rollback")
            raise
            
    @property
    def project(self):
        return DBProject.get(self.DB, self.ProjectID)
        
    @staticmethod
    def reserve_next_available(db, project_id, worker_id):
        # returns reserved handle or None
        c = db.cursor()
        columns = DBFileHandle.columns("h", as_text=True)
        sql = f"""
            update file_handles h
                    set state=%s, worker_id=%s, attempts = h.attempts + 1
                    where h.project_id=%s
                        and row(h.namespace, h.name) in
                        (       select hh.namespace, hh.name
                                        from file_handles hh, replicas r
                                        where hh.project_id=%s
                                                    and hh.state=%s
                                                    and hh.namespace = r.namespace 
                                                    and hh.name = r.name 
                                                    and r.available
                                        order by hh.attempts
                                        limit 1
                        )
                    returning {columns};
        """
        #print(sql)
        try:
            c.execute("begin")
            c.execute(sql, (DBFileHandle.ReservedState, worker_id, project_id, project_id, DBFileHandle.ReadyState))
        except:
            c.execute("rollback")
            raise
        tup = c.fetchone()
        if not tup:
            return None
        c.execute("commit")
        return DBFileHandle.from_tuple(db, tup)
        
    @staticmethod
    def available_handles(db, project_id, state):
        columns = self.columns("h", as_text=True)
        ncols = len(self.Columns)
        c = db.cursor()
        c.execute(f"""
            select {columns}, f.replicas
                from file_handles h
                    inner join files f on f.namespace = h.namespace and f.name = h.name
                where h.project_id=%s and h.state=%s and
                    f.replicas @? '$.* ? (@.available == true)';
                order h.attempts
        """, (project_id, DBFileHandle.InitialState))
        
        for tup in cursor_iterator(c):
            h = DBHandle.from_tuple(db, tup[:-1])
            h.Replicas = tup[-1]
            yield h

    def is_available(self):
        return any(r.Available for r in self.replicas().values())
        
    def done(self):
        self.State = "done"
        self.WorkerID = None
        self.save()
        
    def failed(self, retry=True):
        self.State = self.ReadyState if retry else "failed"
        self.WorkerID = None
        self.save()
        
    def is_active(self):
        return self.State not in ("done", "failed")
        
