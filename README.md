# TranscodeFlex-GCP-Project

Hi Folks, 
Here I bring you TranscodeFlex, a video transcoding Application that uses event-driven invocation for its service to run. It is deployed in GCP and has both serverless and serverfull designs.a

The design:
![Screenshot 2024-04-11 224206](https://github.com/jerilkbestin/TranscodeFlex-GCP-Project-/assets/38150358/9ab143d7-0a1f-487b-8977-c262046a79f6)

Components used:

1.	Platform:
Cloud provider: Google Cloud Platform
Serverfull Instance: Google Compute Engine VM instance
	Machine Type: e2-highcpu-4
	Instance Group: Yes
	Number of Instances: 6
	Load Balancer: Application load Balancer
	Locality Load Balancing Policy: Round-Robin

Serverless Instance: Google Cloud Run
	Instance Configuration: 2 CPU (limit), 4 GB RAM
	Concurrency: 1
	Max instances: 50

Storage: Google Cloud Storage
	Buckets: 4
	Class: Standard
Job Orchestrator: Google workflows
Triggers: Google EventArc
Asynchronous Messenger: Google Pub/Sub with Google Cloud Functions
Web Server: Hosted on Google Compute Engine
Testing Server: Hosted on Google Compute Engine
Logger Function: Google Cloud Functions
Logging: Google Cloud logging
Visualization: Google Metrics Explorer
Dashboard: Google Monitoring

2.	Technology choices:
Application:
-	API build through REST API
Web Server:
-	Frontend through HTML and Bootstrap
-	Backend through python flask
Cloud Functions:
-	Python

3.	Tools:
-	Self-created Automated User Request Testing simulator run on ubuntu VM on GCE.
-	Docker to containerize the application.
-	Flask to create REST API for the application.

Steps to Implement it:

Part 1: Making the container app with Flask:
Files required (inside containerapp):
- entrypoint.sh
- Dockerfile
- app.py
- requirement.txt
- setup.sh

Tools (install them):
- WSL/Linux OS (you can do it in Powershell but my steps need to be changed to Powershell commands)
- Python 3.10.12
- pip3
- docker 25.0.3
- pyinstaller 6.5.0
Docker Image required: https://hub.docker.com/r/intel/intel-optimized-ffmpeg
Steps:
App creation (REST API for container)
1. In WSL, put the files required in the current folder of the shell.
2. cmd: **pyinstaller --onefile --add-data "requirements.txt:." --add-data "setup.sh:." app.py**
3. The final app would be in the /dist folder. copy the file to the current folder.
Container image Creation
1. cmd: **docker build -t myapp_v2:latest .**

GCP Setup:
1. log in to console.cloud.google.com using your Gmail with free credits.
2. Create a new project and add the free credit billing.
3. Enable Compute engine.
4. Go to IAM & Admin --> IAM. You will find that a compute engine default service account was created (with an Editor role). If not we need to create one. Elevate its role to "Owner" if you want to give it full access to all resources.
This would make it easy to continue the project (but not secure).
5. Go to Service accounts --> compute engine account above --> Keys --> Add key --> Create a new key --> JSON --> Download in the same folder as the WSL shell.

This will be the key that enables access to most resources.

Follow this guide to install gcloud in WSL: https://cloud.google.com/sdk/docs/install#deb
# note: instead of "gcloud init", do "gcloud auth login" if login doesn't work.

Please follow this guide for the initial steps of choosing the project and region: https://cloud.google.com/sdk/docs/initializing. I would suggest we stick to one region except if otherwise specified.

Components in GCP to create:
1. Go to console.cloud.google.com

Cloud Storage:
See the following files for configuration. The terraform wouldn't work completely.
destination_bucket_transcoder - see storage --> destination_bucket_transcoder.tf
destination_bucket_transcoder_serverfull - see storage --> destination_bucket_transcoder_serverfull.tf
source_bucket_transcoder - see storage --> source_bucket_transcoder.tf
sample_bucket_transcoder -- see storage --> sample_bucket_transcoder.tf

Upload container image to artifact registry:
1. Enable the artifact registry API.
2. In the same WSL, cmd: **gcloud auth configure-docker**
3. Here is an example of the next command (change accordingly): **docker tag your-local-image:tag us-central1-docker.pkg.dev/your-project-id/your-repo/your-image:your-tag0**
4. cmd: **docker push us-central1-docker.pkg.dev/your-project-id/your-repo/your-image:your-tag**
5. verification cmd: **gcloud artifacts docker images list us-central1-docker.pkg.dev/your-project-id/your-repo**










Reference: https://medium.com/google-cloud/event-driven-ffmpeg-transcoding-a-modern-solution-with-gcp-42995d5c3dbb 
