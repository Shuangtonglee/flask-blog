//页面加载出来歌曲为"晴天"
$(document).ready(function(){
    var songName = "晴天";
    var author = "周杰伦";
    var src = "http://ws.stream.qqmusic.qq.com/C1000039MnYb0qxYhV.m4a?fromtag=0&guid=126548448";
    var imgUrl = "http://imgcache.qq.com/music/photo/album_300/20/300_albumpic_8220_0.jpg";
    var player = new skPlayer({
            listshow: false,
            music: {
                type: 'file',
                source: [
                    {
                        name: songName,
                        author: author,
                        src: src,
                        cover: imgUrl
                    }
                ]
            }
        });
});

//切歌
function fun(){
        var audio = document.getElementsByTagName('audio')[0];
        var songName = $("#songname").val();
        var songApi = "https://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp?g_tk=5381&uin=0&format=jsonp&inCharset=utf-8&outCharset=utf-8&notice=0&platform=h5&needNewCode=1&w="+songName+"&zhidaqu=1&catZhida=1&t=0&flag=1&ie=utf-8&sem=1&aggr=0&perpage=20&n=20&p=1&remoteplace=txt.mqq.all&_=1520833663464"
        $("#songname").val("") ;//清空输入框
        $.ajax({
            url:songApi,
            type:'get',
            dataType:'jsonp',
            jsonp: 'callback',
            jsonpCallback:'callback',
            scriptCharset: 'GBK',
            success: function(data) {
                try {
                    songmid=data.data.song.list[0]["songmid"];
                }
                catch (err){
                    //待实现 input下方提示
                }

                albumid = data.data.song.list[0]["albumid"];
                author = data.data.song.list[0].singer[0]["name"];
                src = 'http://ws.stream.qqmusic.qq.com/C100'+songmid+'.m4a?fromtag=0&guid=126548448';
                imgUrl = "http://imgcache.qq.com/music/photo/album_300/"+albumid%100+"/300_albumpic_"+albumid+"_0.jpg";
                var player = new skPlayer({
                    listshow: false,
                    music: {
                        type: 'file',
                        source: [
                            {
                                name: songName,
                                author: author,
                                src: src,
                                cover: imgUrl
                            }
                        ]
                    }
                });
                audio.src = src;
                $(".skPlayer-cover").attr("src",imgUrl);
                $(".skPlayer-name").text(songName);
                $(".skPlayer-author").text(author);
                $(".skPlayer-list-name").text(songName);
                $(".skPlayer-list-name").attr("title",songName);
                $(".skPlayer-list-author").text(author);
                $(".skPlayer-list-author").attr("title",author);
                $(".skPlayer-cover").removeClass("skPlayer-pause"); //切歌时按钮切换
                $(".skPlayer-play-btn").removeClass("skPlayer-pause");
            }
        })
}/**
* Created by li on 6/27/2018.
*/
