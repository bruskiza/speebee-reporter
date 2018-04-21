FROM alpine:3.5
ARG PANDAS_VERSION=0.22.0
RUN apk add --no-cache python-dev py2-pip && \
    apk add --no-cache --virtual .build-deps g++ && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip install numpy==1.14.0 && \
    pip install pandas==${PANDAS_VERSION} && \
    apk del .build-deps
RUN pip install beebotte
COPY runner.ash /app/bin/runner.ash
COPY reporter.py /app/bin/reporter.py

ENTRYPOINT ["/app/bin/runner.ash"]
