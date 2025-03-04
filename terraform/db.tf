resource "mongodbatlas_cluster" "cluster-test" {
  project_id = "burendo-handbook-cluster"
  name       = "burendo-handbook-cluster"

  # Provider Settings "block"
  provider_name               = "TENANT"
  backing_provider_name       = "AWS"
  provider_region_name        = "EU_WEST_2"
  provider_instance_size_name = "M0"
}
