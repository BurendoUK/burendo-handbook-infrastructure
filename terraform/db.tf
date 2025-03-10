resource "mongodbatlas_cluster" "handbook-db" {
  project_id = "67c806f87ceec5230502cfc1"
  name       = "burendo-handbook-db"

  # Provider Settings "block"
  provider_name               = "TENANT"
  backing_provider_name       = "AWS"
  provider_region_name        = "EU_WEST_1"
  provider_instance_size_name = "M0"
}

resource "mongodbatlas_database_user" "handbook-user" {
  username           = local.mongodb_user
  password           = local.mongodb_password
  project_id         = "67c806f87ceec5230502cfc1"
  auth_database_name = "admin"

  roles {
    role_name     = "readWriteAnyDatabase"
    database_name = "admin"
  }

  scopes {
    name = mongodbatlas_cluster.handbook-db.name
    type = "CLUSTER"
  }
}
