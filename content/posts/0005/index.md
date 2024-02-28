---
title: OCI Function with a custom image
date: 2023-05-12T19:00:00+01:00
draft: false
tags:
  - functions
categories:
  - serverless
cover:
  alt: OCI Function with a custom image
  caption: OCI Function with a custom image
  image: static/fn.webp  
  relative: true
aliases:
  - "/2023/05/oci-function-with-a-custom-image/"
---

As we have seen from my other [articles]({{< ref "/tags/functions/" >}}), it is possible to use the FN project with different programming languages using predefined container images, the officially supported languages are:

* go
* java
* Node.js
* ruby
* Python
* C#

you can do it with the runtime directive, for example:

```console
fn init --runtime python test
```

the command will produce a func.yaml file of this type

{{< highlight yaml "linenos=table" >}}
schema_version: 20180708
name: hello
version: 0.0.1
runtime: python
build_image: fnproject/python:3.9-dev
run_image: fnproject/python:3.9
entrypoint: /python/bin/fdk /function/func.py handler
memory: 256
{{< / highlight >}}


However, in some cases, the predefined images are not sufficient, either for extra language support, extra drivers, or other missing tools.

To solve this problem it is possible to use your own Dockerfile in your own custom environment, we can extend the basic FN image or start from a totally different image.

As a demo, I created [this example](https://github.com/enricopesce/fn-examples/tree/main/customimage) in the specific the func.yaml file will look like this:

{{< highlight yaml "linenos=inline" >}}
schema_version: 20180708
name: customimage
version: 0.0.1
runtime: docker
memory: 256
{{< / highlight >}}


in this way, FN uses a local Dockerfile saved at the same level to create the function execution environment, from the example the Dockerfile will look like this:

{{< highlight docker "linenos=inline,hl_lines=1 10-12" >}}
FROM fnproject/python:3.9
WORKDIR /function
ADD requirements.txt /function/

RUN pip3 install --target /python/ --no-cache --no-cache-dir -r requirements.txt &&\
    rm -fr ~/.cache/pip /tmp* requirements.txt func.yaml Dockerfile .venv &&\
    chmod -R o+r /python

# install Oracle database client
RUN microdnf install oracle-instantclient-release-el8 &&\
    microdnf install oracle-instantclient-basic &&\
    microdnf clean all

ADD . /function/

RUN chmod -R o+r /function

ENV PYTHONPATH=/function:/python

ENTRYPOINT ["/python/bin/fdk", "/function/func.py", "handler"]
{{< / highlight >}}

In this Dockerfile we have customized the official Python 3.9 with Oracle's database client.

It is possible to do local tests without having to distribute the image in the remote repository every time using the specific option --local in the deployment phase

```console
fn deploy --app app --local
```

by running the FN server locally it will be possible to execute the function code in the same way as on the OCI but locally

Then launch on a separate terminal session the FN server instance:

```console
fn start
```

and in another the classic invocation command, for example

```console
echo -n '{"name": "Oracle"}' | fn invoke app hello
```