resource "google_storage_bucket" "destination_bucket_transcoder_serverfull" {
  force_destroy               = false
  location                    = "US-WEST2"
  name                        = "destination_bucket_transcoder_serverfull"
  project                     = "spheric-rhythm-414505"
  public_access_prevention    = "inherited"
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}