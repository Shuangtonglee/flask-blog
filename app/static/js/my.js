/*================================
=====2016-7-16 power by zzc=========
================================*/


$(document).ready(function(){
	//滑动效果	
	$(".drop1").mouseenter(function(){

		$(".drop1-nav").css({"-webkit-animation": "zuo1 0.8s","animation": "zuo1 0.8s"}).show();

	}).mouseleave(function(){
		 $(".drop1-nav").css({"-webkit-animation": "zuo2 0.8s","animation": "zuo2 0.8s"});
		 setTimeout(function(){
			   $(".drop1-nav").hide();
			},500);

	});

    $(".drop2").mouseenter(function(){

		$(".drop2-nav").css({"-webkit-animation": "zuo1 0.8s","animation": "zuo1 0.8s"}).show();

	}).mouseleave(function(){
		 $(".drop2-nav").css({"-webkit-animation": "zuo2 0.8s","animation": "zuo2 0.8s"});
		 setTimeout(function(){
			   $(".drop2-nav").hide();
			},500);

	});
        //文字滚动
    $(function () {

        var _wrap = $('.multline');//定义滚动区域
        var _interval = 3000;//定义滚动间隙时间
        var _moving;//需要清除的动画
        _wrap.hover(function () {
            clearInterval(_moving);//当鼠标在滚动区域中时,停止滚动
        }, function () {
            _moving = setInterval(function () {
                var _field = _wrap.find('li:first');//此变量不可放置于函数起始处，li:first取值是变化的
                var _h = _field.height();//取得每次滚动高度
                _field.animate({ marginTop: -_h + 'px' }, 500, function () {//通过取负margin值，隐藏第一行
                    _field.css('marginTop', 0).appendTo(_wrap);//隐藏后，将该行的margin值置零，并插入到最后，实现无缝滚动
                })
            }, _interval)//滚动间隔时间取决于_interval
        }).trigger('mouseleave');//函数载入时，模拟执行mouseleave，即自动滚动
        if ($(".multline li").length <= 1)//小于等于1条时，不滚动
        {
            clearInterval(_moving);

        }

    });


    $(".mail-btn").click(function(){
        var sharbox = $(".sharebox");
        if(sharbox.css("display") == "block"){
            sharbox.hide()
        }
        $(".mail").show();
			});

    $(".el-remove").click(function(){

        $(".mail").hide();
        $(".sharebox").hide();
			});


    $(".share").click(function(){
        var mail = $(".mail");
        if(mail.css("display") == "block"){
            mail.hide()
        }

        $(".sharebox").show();
			});

    $(".fx-btn").click(function(){
        $(".arc-position").show();
			});

    $(".flash").hide(3000);

    //TAB切换
/*		$(".mytab a").click(function(){
			var index=$(this).index();
			$(this).addClass("tab-active").siblings().removeClass("tab-active");
			$(this).parents(".mytab").find("ul").eq(index).show().siblings('ul').hide();

		});*/


        $(".title-1").click(function(){
            $(".title-1").addClass("title-active");
            $(".title-2").removeClass("title-active");
            $(".comment-2").hide();
            $(".comment-1").show();
        });

        $(".title-2").click(function(){
            $(".title-1").removeClass("title-active");
            $(".title-2").addClass("title-active");
            $(".comment-2").show();
            $(".comment-1").hide();
        })

});//END Document ready
		
//JS区域
