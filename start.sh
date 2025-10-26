  #!/bin/bash
  docker run -d --restart always --name aerial-ace --env-file /root/aerial-ace/.env staticaron/aerial-ace:latest
