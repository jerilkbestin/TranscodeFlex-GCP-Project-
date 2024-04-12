resource "google_storage_bucket" "sample_bucket_transcoder" {
  force_destroy            = false
  location                 = "US-WEST2"
  name                     = "sample_bucket_transcoder"
  project                  = "spheric-rhythm-414505"
  public_access_prevention = "inherited"
  storage_class            = "STANDARD"
}