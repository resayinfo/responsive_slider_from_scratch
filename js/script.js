$(function() {

    $('.slide').on('mouseenter', '.fa', function() {
        $(this).removeClass('fa-circle-o');
        $(this).addClass('fa-circle');
    });

    $('.slide').on('mouseleave', '.fa', function() {

        var image_index = $('.slider').css('background-image');
        image_index = parseInt(image_index.split('/').pop().split('.')[0].split('-')[1]);
        image_index -= 1;

        var slide_index = parseInt($(this).index());

        if(image_index !== slide_index)
        {
            $(this).removeClass('fa-circle');
            $(this).addClass('fa-circle-o');
        }

    });

    $('.slide').on('click', '.fa', function() {
        var index = $(this).index() + 1;
        var path = 'url(images/slider-0' + index + '.jpg)'; 

        $('.slider').css({
            backgroundImage: path
        });
        
        $('.slide .fa').removeClass('fa-circle');
        $('.slide .fa').addClass('fa-circle-o');
        $(this).addClass('fa-circle');
    });

    $.getJSON('/images/content.json', function(_data) {

        data = _data.content;

        for(i=0; i<data.length; i++)
        {
            if(i === 0)
            {
                $('.slide').append(
                    '<span class="fa fa-circle"></span>'
                );
                continue;
            }

            $('.slide').append(
                '<span class="fa fa-circle-o"></span>'
            );
        }

    });

}());
