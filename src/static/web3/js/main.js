"use strict";

$(window).on('load', function () {

    $('form.form__validator').on('input', 'input, textarea', function () {

        let allFieldsFilled = true;

        $('input, textarea').each(function() {
            if ($(this).val() === '') {
                allFieldsFilled = false;
            }
        });

        if (allFieldsFilled) {
            $('button').prop('disabled', false);
            $(this).addClass('border-on')
        } else {
            $('button').prop('disabled', true);
            $(this).removeClass('border-on')
        }
    })

    $('form.form__validator-2').on('change', 'input[type="radio"]', function () {

        let allRadiosChecked = false;

        $('input[type="radio"]').each(function() {
            if ($(this).prop('checked')) {
                allRadiosChecked = true;
                $('.rate__box').find('.rate__list').slideUp('200');
                $(this).closest('.rate__box').find('.rate__list').slideDown('200');
                return false;
            } else {
                $(this).closest('.rate__box').find('.rate__list').slideUp('200');
            }
        });

        if (allRadiosChecked) {
            $('button').prop('disabled', false);
            $(this).addClass('in-on');
        } else {
            $('button').prop('disabled', true);
            $(this).removeClass('in-on');
        }
    });


    $('.popup .close').click(function (event){
        event.preventDefault();
        $('.popup').fadeOut('200');
        setTimeout(()=> {
            $('.popup__back').slideUp('200');
        }, 250)
    })



    $('.form__tel, .form__tel-2').inputmask("+\\9\\98 (99) 999 99 99");

    $('#prices__summ, .prices__general').inputmask({
            groupSeparator: " ",
            alias: "numeric",
            placeholder: "0",
            autoGroup: true,
            digits: 0,
            digitsOptional: false,
            clearMaskOnLostFocus: false
    });

    $('.prices__before').inputmask("decimal", {
        groupSeparator: " ",
        alias: "numeric",
        placeholder: "0",
        autoGroup: true,
        digits: 0,
        digitsOptional: false,
        clearMaskOnLostFocus: false
    });



    AOS.init({
        // Global settings:
        disable: false, // accepts following values: 'phone', 'tablet', 'mobile', boolean, expression or function
        startEvent: 'DOMContentLoaded', // name of the event dispatched on the document, that AOS should initialize on
        initClassName: 'aos-init', // class applied after initialization
        animatedClassName: 'aos-animate', // class applied on animation
        useClassNames: false, // if true, will add content of `data-aos` as classes on scroll
        disableMutationObserver: false, // disables automatic mutations' detections (advanced)
        debounceDelay: 50, // the delay on debounce used while resizing window (advanced)
        throttleDelay: 99, // the delay on throttle used while scrolling the page (advanced)


        // Settings that can be overridden on per-element basis, by `data-aos-*` attributes:
        offset: 120, // offset (in px) from the original trigger point
        delay: 0, // values from 0 to 3000, with step 50ms
        duration: 400, // values from 0 to 3000, with step 50ms
        easing: 'ease', // default easing for AOS animations
        once: false, // whether animation should happen only once - while scrolling down
        mirror: false, // whether elements should animate out while scrolling past them
        anchorPlacement: 'top-bottom', // defines which position of the element regarding to window should trigger the animation

    });

    // let selector = document.getElementsByClassName("form__tel");
    // let selector2 = document.getElementsByClassName("form__tel-2");
    // let im = new inputmask("+\\9\\98(99)999-99-99");
    // im.inputmask(selector);


    $('.tel__add').click(function (event) {
        event.preventDefault();
        $('.tel__adding').append(`<label for="tel__input" class="tel__box">
            <input type="tel"
                   id="tel__input-2"
                   name="tel-2"
                   required
                   class="form__tel-2 general-R general__input"
                   placeholder="+998 (99) 999-99-99"
                   pattern="^[0-9-+\\s()]*$">
          </label>`);
        // im.mask(selector2);
        $('.form__tel, .form__tel-2').inputmask("+\\9\\98 (99) 999 99 99");
        $(this).remove()
    });

    let swiperFinished = new Swiper(".finished__slider", {
        slidesPerView: 1,
        spaceBetween: 30,
        navigation: {
            nextEl: ".finished__slider-next",
            prevEl: ".finished__slider-prev",
        },
        pagination: {
            el: ".finished__slider-pagination",
        },
    });

    // $('.photo__form input[type=file]').change(function(){
    //     let id = $(this).attr("data-up");
    //     let newimage = new FileReader();
    //     newimage.readAsDataURL(this.files[0]);
    //     newimage.onload = function(e){
    //         $('.photo__img-' + id ).css('background-image', 'url(' + e.target.result + ')' );
    //     }
    // });

    function uploadImages() {
        const maxLength = 4;
        const imgArray = [];
        const uploadInputfile = $('.upload__inputfile');

        uploadInputfile.each((index, element) => {
            const imgWrap = $(element).closest('.photo__form').find('.photo__container');

            $(element).on('change', (event) => {
                const files = event.target.files;
                const filesArr = Array.from(files);

                filesArr.forEach((file) => {
                    if (!/^image\//.test(file.type) || imgArray.length >= maxLength) {
                        return;
                    }


                    const formData = new FormData();
                    formData.append('file', file);
                    $.ajax({
                        url: window.location.origin+'/api/v1/file/upload/',
                        type: 'POST',
                        data: formData,
                        processData: false,
                        contentType: false,
                        success: function (response) {
                        if (response) {
                            console.log(">>>>", response);
                            imgArray.push(file);

                            const reader = new FileReader();
                            reader.onload = (e) => {
                        const input = $('<input>', { type: 'file', value: '', name: 'photo[]', class: 'upload__inputfile' });
                        const html = `
                            <div class="photo__container-box">
                              <div class="img-bg"
                              style="background-image: url(${e.target.result})"
                              data-number="${$(".upload__img-close").length}"
                              data-file="${file.name}">
                                <div class="upload__img-close"></div>
                                <input type="text" value="`+ response['data']['file_url'] +`" name="file" style="display:none">
                                <input type="text" value="`+ response['data']['versatil_url'] +`" name="versatil_file" style="display:none">
                              </div>
                            </div>`;

                        imgWrap.append($(html));
                            }
                    reader.readAsDataURL(file);
                            $('button').prop('disabled', false);
                            } else {
                            $('button').prop('disabled', true);
                            }

                        },
                        error: function (xhr, status, error) {
                            console.log(error);
                        }
                    });
                });
            });
        });

        $('body').on('click', ".upload__img-close", (event) => {
            const file = $(event.target).closest('.img-bg').data("file");
            imgArray.splice(imgArray.findIndex(f => f.name === file), 1);
            $(event.target).closest('.photo__container-box').remove();
        });
    }

    uploadImages();



     $('.control__close').click(function (event) {
//         event.preventDefault();
//
//         enableClosingConfirmation();
        window.location.href = "https://t.me/Avtopikbot"
     })

});
