mkdir -p venmo_oracle/pip_wheels
cd venmo_oracle
pip3 install wheel
pip3 wheel --wheel-dir pip_wheels -r requirements.txt -f https://download.pytorch.org/whl/cpu/torch_stable.html
tar -czvf - pip_wheels | split -b 32M - pip_wheels.tar.gz
rm -rf ./pip_wheels
cat $(find . -type f | sort) | sha256sum | awk '{print $1}'
