const dbName = 'mongo';
const userName = 'app_user';
const userPwd = 'verystrongpassword';

const appdb = db.getSiblingDB(dbName);

const existing = appdb.getUser(userName);
if (!existing) {
  appdb.createUser({
    user: userName,
    pwd: userPwd,
    roles: [{ role: 'readWrite', db: dbName }],
  });
  print(`User ${userName}@${dbName} created`);
} else {
  print(`User ${userName}@${dbName} already exists, skipping`);
}
