# Quote2Clip
Utility script for extracting clips based on partial or exact quotes.


### Usage
`python main.py query [n_clips] [m_context]`

`query` : string of wanted text <br/>
`n_clips` : positive integer, outputs `n` best matches <br/>
`m_context` : non-zero integer, includes `m` sequences of text before or after the query, depending on the sign of `m` <br/>

Example:

```python main.py "ice cube" 3 -2``` <br/>
Matches "ice cube", includes 2 entries before the entry containing "ice cube", selects the best 3 matches.

### Requirements
`ffmpeg-python`

##### Folder structure:
```
Root/
├──Output/
├──Subtitles/
|  ├──S01/
│  │  ├──episode_1.srt
│  │  └──... 
│  ├──S02/
│  └──... 
└──Video/
   ├──S01/
   │  ├──episode_1.mkv
   │  └──...
   └──S02/ 
   ```
