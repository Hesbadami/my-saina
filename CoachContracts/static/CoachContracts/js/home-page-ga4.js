import { ItemConstructor, EItemListInfo } from './ecommerce-utils.js'

$(document).ready(function () {
    // init gathering data from view_item_list Repetitive Expertise list
    // WE ONLY NEED DOCTOR ITEMS TO SEND TO E-COMMERCE - SO WE COMMENT THIS METHOD TO BE BACKWARD COMPATIBLE
    // InitRepetitiveExpertiseViewItemList();
    
    // init gathering data from select_item Repetitive Expertise list
    // WE ONLY NEED DOCTOR ITEMS TO SEND TO E-COMMERCE - SO WE COMMENT THIS METHOD TO BE BACKWARD COMPATIBLE
    // InitRepetitiveExpertiseSelectItem();
    
    // init gathering data from view_item_list Doctors Accompany list
    InitDoctorsAccompanyViewItemList();
    // init gathering data from select_item Doctors Accompany list
    InitDoctorsAccompanySelectItem();
})

// get current position into the list 
function getItemPosition(item) {
    var position = 0
    var displayedItems = $(item).parent().children()
    var itemPosition = displayedItems.index(item)
    position = itemPosition;
    return position
}

function InitRepetitiveExpertiseViewItemList() {

    function CheckPushData(element) {
        if (element.attr('data-ecm-ga4-visited') != 1) {
            element.attr('data-ecm-ga4-visited', 1)
            PushRepetitiveExpertiseDataToDataLayer("view_item_list", element)
        } else {
            return;
        }
    }

    var targets = document.querySelectorAll(".flickity-spacing-call-doctor");
    $(targets).each(function () {
        var item = this
        var observer = new MutationObserver(function () {
            CheckPushData($(item))
        });
        observer.observe(this, {
            attributes: true
        });
    })


    $(window).on('scroll', function () {
        $(targets).each(function () {
            if ($(this).isInHorizontalViewport() && $(this).isInViewport()) {
                CheckPushData($(this))
            }
        })
    });


}

function InitRepetitiveExpertiseSelectItem() {
    var isDragging = false;
    var element = $(".flickity-spacing-call-doctor");

    element.on('pointerdown', function () {
        isDragging = false;
    });

    element.on('pointermove', function () {
        isDragging = true;
    });

    element.on('pointerup', function () {
        var wasDragging = isDragging;
        isDragging = false;
        if (!wasDragging) {
            PushRepetitiveExpertiseDataToDataLayer('select_item', $(this))
        }
    });
}

function PushRepetitiveExpertiseDataToDataLayer(event, target) {
    var item = getRepetitiveExpertiseItemData(target)
    item.item_list_id = EItemListInfo['home_page_repetitive_expertise_slider'].item_list_id;
    item.item_list_name = EItemListInfo['home_page_repetitive_expertise_slider'].item_list_name;
    dataLayer.push({ ecommerce: null });
    dataLayer.push({
        event: event,
        ecommerce: {
            items: [item]
        }
    });
}

function getRepetitiveExpertiseItemData(target) {

    // get affiliation data
    var affiliation = Cookies.get("faId")

    // get current position into the list 
    var position = getItemPosition(target)

    var newItem = new ItemConstructor(target.attr('data-category-id'), target.attr("data-category-slug"))
    newItem.affiliation = affiliation || '';
    newItem.index = position;
    newItem.item_category2 = target.attr('data-category-title');

    return newItem;
}

// ------------------------------------------------ Doctors ready to accompany
function InitDoctorsAccompanyViewItemList() {
    function CheckPushData(element) {
        if (element.attr('data-ecm-ga4-visited') != 1) {
            element.attr('data-ecm-ga4-visited', 1)
            PushDoctorsAccompanyDataToDataLayer("view_item_list", element)
        } else {
            return;
        }
    }

    var targets = document.querySelectorAll(".flickity-spacing-doctor-list");
    $(targets).each(function () {
        var item = this
        var observer = new MutationObserver(function () {
            CheckPushData($(item))
        });
        observer.observe(this, {
            attributes: true
        });
    })


    $(window).on('scroll', function () {
        $(targets).each(function () {
            if ($(this).isInHorizontalViewport() && $(this).isInViewport()) {
                CheckPushData($(this))
            }
        })
    });
}

function InitDoctorsAccompanySelectItem() {

    var element = $(".doctor-list-item .detail-info > a");

    var isDragging = false;
    element.on('pointerdown', function () {
        isDragging = false;
    });

    element.on('pointermove', function () {
        isDragging = true;
    });

    element.on('pointerup', function () {
        var wasDragging = isDragging;
        isDragging = false;
        if (!wasDragging) {
            PushDoctorsAccompanyDataToDataLayer('select_item', $(this).parents('.top-interaction-box-transform'))
        }
    });

}

function PushDoctorsAccompanyDataToDataLayer(event, target) {
    var item = getDoctorsAccompanyItemData(target)
    item.item_list_name = EItemListInfo['home_page_doctors_accompany_slider'].item_list_name;
    item.item_list_id = EItemListInfo['home_page_doctors_accompany_slider'].item_list_id;

    dataLayer.push({ ecommerce: null });
    dataLayer.push({
        event: event,
        ecommerce: {
            items: [item]
        }
    });
}

function getDoctorsAccompanyItemData(target) {
    // get affiliation data
    var affiliation = Cookies.get("faId")

    // get current position into the list 
    var position = getItemPosition(target)

    var newItem = new ItemConstructor(target.attr('data-id'), target.attr("data-name"))
    newItem.affiliation = affiliation || '';
    newItem.index = position;
    // newItem.item_category2 = target.attr('data-category');
    newItem.item_category = target.attr('data-doctorspecialty') || '';
    newItem.item_category2 = target.attr('data-doctorabovespecialty') || '';

    return newItem;
}

//Utils
$.fn.isInViewport = function (offsetPercent) {
    var offsetPercentOfElement = ((offsetPercent ? (100 - offsetPercent) : 10) / 100) * $(this).outerHeight()
    var elementTop = $(this).offset().top; // faseleye balaye element az balaye document
    var elementBottom = elementTop + $(this).outerHeight(); // majmooe elementTop ba heighte element
    var viewportTop = $(window).scrollTop() + offsetPercentOfElement; // $(window).scrollTop() yani Meghdari ke az bala scroll shode
    var viewportBottom = viewportTop + $(window).height(); // majmooe viewportTop ba heighte safhe namayesh
    return elementTop > viewportTop && elementBottom < viewportBottom;
};

//Utils
$.fn.isInHorizontalViewport = function (offsetPercent) {
    // var itemWidth = $(this).outerWidth()
    var itemLeftPosition = $(this).offset().left;
    // var itemRightPosition = $(targets).offset().right;
    var windowWidth = $(window).width()
    return itemLeftPosition > 0 && itemLeftPosition < windowWidth
};
    