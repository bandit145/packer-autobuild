import psycopg2

class Database:

	#connection is a dict {user:user,password:password,host:host,ssl:true/false,}
	def __init__(self,db_server,**kwargs):
		try:
			self.conn = psycopg2.connect(**kwargs['connection'])
		except psycopg2.Error as error:
			print(error)

	#utility methods
	def _run_sql_query_(self,sql_query,data,return_required=False):
		cursor = self.conn.cursor()
		try:
			if return_required:
				cursor.execute(sql_query,data)
				data = cursor.fetchall()
				cursor.close()
				return data
			else:
				cursor.execute(sql_query,data)
				cursor.commit()
				cursor.close()
		except psycopg2.Error as error:
			print(error.pgerror)

	#user ops
	def _select_username_(self,**kwargs):
		if 'username' in kwargs.values():
				user = kwargs['username']
		elif 'email' in kwargs.values():
			user = kwargs['email']
		return user

	def add_local_user(self,username,email,password):
		#hash password
		self._run_sql_query_('INSERT INTO (username,email,password) local_users (%s,%s,%s)'
			,(username,email,password))


	def delete_local_user(self,**kwargs):
		user = self._select_username_(**kwargs)
		self._run_sql_query_('user := %s; DELETE FROM local_users WHERE username = user OR email = user'
			,(user))

	def get_local_user_groups(self,**kwargs)
		user = self._select_username_(**kwargs)
		self._run_sql_query_('user := %s; Select group_name from groups WHERE  ')


	def update_local_user_email(self,**kwargs):
		user = self._select_username_(**kwargs)
		self._run_sql_query_('user := %s; UPDATE local_users SET email = %s WHERE username = user or email = user',(user))
	
	def add_runner(self, host_name, group_name):
		self._run_sql_query_('INSERT into runners (host_name,group_name) values (%s,%s)',(host_name,group_name))

	def change_runner_group(self, host_name, group_name):
		self._run_sql_query_('UPDATE runners SET group_name = %s WHERE host_name = %s'(group_name, host_name))

	def delete_runner(self, host_name):
		self._run_sql_query_('DELETE from runners WHERE host_name = %s',(host_name))

	def add_repo(self, repo_name, repo_url, branch):
		self._run_sql_query_('INSERT into repos (repo_url, repo_name, branch)',(repo_name, repo_url, branch))

	def del_repo(self, repo_id):
		self._run_sql_query_('DELETE from repos WHERE repo_id = %s',(repo_id))
	#maybe no edit repo

