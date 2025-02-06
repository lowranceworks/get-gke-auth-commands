import subprocess
import json

def get_gke_commands():
   # Get projects list
   projects = subprocess.check_output(
       ["gcloud", "projects", "list", "--format=json"]
   )
   projects = json.loads(projects)
   
   commands = []
   for project in projects:
       project_id = project["projectId"]
       try:
           clusters = subprocess.check_output([
               "gcloud", "container", "clusters", "list",
               f"--project={project_id}",
               "--format=json"
           ])
           clusters = json.loads(clusters)
           
           for cluster in clusters:
               cmd = f"gcloud container clusters get-credentials {cluster['name']} --region={cluster['location']} --project={project_id}"
               commands.append(cmd)
               
       except subprocess.CalledProcessError:
           continue
           
   return commands

if __name__ == "__main__":
   for cmd in get_gke_commands():
       print(cmd)
