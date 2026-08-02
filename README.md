This is a very simple script with a *reasonable* amount of customization available that allows you to play sounds in the background by pressing assigned keys 

**This script requires ffplay installed and added to path**, verify if you have ffplay installed by running

```ps
ffplay -version
```

# Setup

```ps
git clone https://github.com/vrceao/soundboard
cd soundboard
py -m pip install -r requirements.txt
py .\main.py
```

# Customization

After cloning, you're using the default config.

**F1** - vine,
**F2** - fumo

- Check out **preferences.jsonc** to customize everything including the keybindings
- Put your sounds in the `logs/` directory