# Concourse AWX Resource

A [Concource CI](https://concourse-ci.org/) custom resource for [Ansible AWX](https://github.com/ansible/awx).
Docker images are located [here](https://quay.io/repository/mamercad/concourse-awx-resource), the `Dockerfile` is in the root of this repository.
Currently, the resource supports [AWX Job Templates](https://docs.ansible.com/ansible-tower/latest/html/userguide/job_templates.html) and [Workflow Job Templates](https://docs.ansible.com/ansible-tower/latest/html/userguide/workflow_templates.html).

## Example Pipeline

```yaml
resource_types:
  - name: awx-workflow-resource
    type: docker-image
    source:
      repository: quay.io/mamercad/concourse-awx-resource

resources:
  - name: awx
    type: awx-workflow-resource
    source:
      awx:
        endpoint: ((TOWER_HOST))
        auth: Bearer ((TOWER_OAUTH_TOKEN))

jobs:
  - name: awx-job
    plan:
      - put: awx
        params:
          awx:
            type: job_templates
            id: ((TOWER_JOB_TEMPLATES))
            debug: false
      - put: awx
        params:
          awx:
            type: workflow_job_templates
            id: ((TOWER_WORKFLOW_JOB_TEMPLATES))
            debug: false
```

## Screenshot

All of the job results will be returned, here's a screenshot to give you a feel:

![Screenshot of Concourse AWX Resource](screenshot.png)
## License

MIT © Mark Mercado <<mamercado@gmail.com>>
