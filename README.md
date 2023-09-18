# installing script

```bash
git clone https://github.com/BlackBoxBanner/epub2audio.git ~/epub2audio   
```

then run

```bash
pip install ~/epub2audio -r requirements.txt
```

The command above will install python package dependencies from requirements.txt

then run

```bash
chmod +x epub2audio
```

and

add the following line to your `.rc` file
```bash
export PATH="~/epub2audio/:$PATH"
```
