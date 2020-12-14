FROM alpine:latest

ARG USERNAME=prowler
ARG USERID=34000

RUN addgroup -g ${USERID} ${USERNAME} && \
    adduser -s /bin/sh -G ${USERNAME} -D -u ${USERID} ${USERNAME} && \
    apk --update --no-cache add python3 py3-pip bash curl jq file coreutils git && \
    pip3 install --upgrade pip && \
    pip3 install awscli boto3 detect-secrets && \
    git clone https://github.com/toniblyx/prowler

WORKDIR /prowler

RUN chown -R prowler . 

ENTRYPOINT ["./prowler"]