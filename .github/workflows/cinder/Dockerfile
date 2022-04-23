FROM fedora:32 as build-container
LABEL org.opencontainers.image.source https://github.com/facebookincubator/cinder
RUN dnf install -y g++ git zlib-devel bzip2 bzip2-devel readline-devel sqlite \
                   sqlite-devel openssl-devel xz xz-devel libffi-devel

# Build container
FROM build-container as build
COPY --chmod=r . /cinder-build
WORKDIR /cinder-build/build
RUN ../configure --prefix=/cinder
RUN make -j$(nproc) VERBOSE=1
RUN make install
RUN strip /cinder/bin/python3.8
# These libraries are very big and generally are not needed.
RUN rm /cinder/lib/libpython3.8_static.a
RUN rm /cinder/lib/python3.8/config-3.8-x86_64-linux-gnu/libpython3.8_static.a

# Cinder installed to /cinder
FROM fedora:32 as runtime
COPY --from=build /cinder /cinder
COPY --from=build /cinder-build/Tools /cinder/Tools

# Cinder Explorer
FROM runtime as explorer
# Run server as appuser
RUN groupadd -g 1001 appuser
RUN useradd --create-home --shell /bin/bash --gid appuser appuser
USER appuser
WORKDIR /home/appuser
CMD /cinder/bin/python3 /cinder/Tools/scripts/ir_viz/gen.py explorer --port 8000 --runtime /cinder/bin/python3
EXPOSE 8000
