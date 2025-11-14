db.createUser({
  user: "electrofix_user",
  pwd: "electrofix_pass",
  roles: [
    {
      role: "readWrite",
      db: "electrofix"
    }
  ]
});

db.createCollection("users");
db.createCollection("services");
db.createCollection("bookings");
db.createCollection("technicians");