# music-metadata-python
A small python tool that allows you to set automatically set metadata to your songs, powered by Deezer's API

## Using

```python


mmm = MP3MetadataMaker("/directory_containing_songs")
mmm.set_api_key("YOUR_API_KEY")
mmm.process()

```


