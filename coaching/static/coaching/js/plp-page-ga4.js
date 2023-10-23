import { ItemConstructor, EItemListInfo, queryStringToJSON } from './ecommerce-utils.js'

$(document).ready(function () {
    // init gathering data from view_item_list plp list event 
    InitPlpViewItemList();
    // init gathering data from select_item plp list event
    InitPlpSelectItem();
    // init gathering data from view_item_list dr suggestion event 
    InitPlpDrSuggestionViewItem();
    // init gathering data from select_item dr suggestion event
    InitPlpDrSuggestionSelectItem();
})

// get current position into the list 
function getItemPosition(item) {
    var position = 0
    var displyedItems = $(item).parent().children().filter(function () {
        return $(this).css('display') !== 'none'
    })
    var itemPosition = displyedItems.index(item)
    position = itemPosition;
    return position
}

//------------------------------ 
function getPlpItemData(target) {
    
    var subCategory = getUrlInfo().subCategory
    // get affiliation data
    var affiliation = Cookies.get("faId")

    // get current position into the list 
    var position = getItemPosition(target)

    var categoryPlusSubCategoryCaption = $("#hidden-ecm-category-id").attr("data-cat-caption");
    var doctorExpertise = $(target).attr('data-expertise');
    var doctorSuperExpertise = $(target).attr('data-superExpertise');
    // docObj["category"] = doctor_item_tag.attr("data-category");
    var newItem = new ItemConstructor(target.attr("data-id"), target.attr("data-name"))
    newItem.affiliation = affiliation || '';
    newItem.index = position;
    newItem.item_category = doctorExpertise || '';
    newItem.item_category2 = doctorSuperExpertise || '';
    newItem.item_list_id = EItemListInfo['consultation_plp_list'].item_list_id + '_' + subCategory;
    newItem.item_list_name = EItemListInfo['consultation_plp_list'].item_list_name + categoryPlusSubCategoryCaption;

    return newItem;
}

//-----------------------------push data to from datalayer of google tag manager
function PushPlpViewItemListData(doctor_item_tag, list) {

    //check is before viewed
    if (doctor_item_tag.attr("data-ecm-ga4-view") == "1")
        return;
    doctor_item_tag.attr("data-ecm-ga4-view", "1")

    //get doctor object from html tag
    var item = getPlpItemData(doctor_item_tag, list)
    // item.item_list_id = EItemListInfo['consultation_plp_list'].item_list_id;
    // item.item_list_name = EItemListInfo['consultation_plp_list'].item_list_name;

    dataLayer.push({ ecommerce: null });
    dataLayer.push({
        event: "view_item_list",
        ecommerce: {
            items: [item]
        }
    });
}

//------------------------------ Init Doctors In Category view_item_list
function InitPlpViewItemList() {
    var doctorCardElements = document.querySelectorAll(".rowItem_LC.doctorId");
    $(window).on('load scroll', function () {
        $(doctorCardElements).each(function () {
            if ($(this).isInViewport()) {
                if ($(this).attr('data-ecm-ga4-visited') != 1 && $(this).css('display') != 'none') {
                    $(this).attr('data-ecm-ga4-visited', 1)
                    PushPlpViewItemListData($(this))
                } else {
                    return;
                }
            }
        })
    });
}

//-------------------------------Push Data Click Of  Doctor List In Category Page
function PushPlpSelectItemData(productObj, list) {
    var item = getPlpItemData(productObj, list)
    // item.item_list_id = EItemListInfo['consultation_plp_list'].item_list_id;
    // item.item_list_name = EItemListInfo['consultation_plp_list'].item_list_name;

    dataLayer.push({ ecommerce: null });
    dataLayer.push({
        event: "select_item",
        ecommerce: {
            items: [item]
        }
    });


    dataLayer.push({ ecommerce: null, activePlan: undefined, gender: undefined, hasInsurance: undefined, isOnline: undefined, specialization: undefined, upperSpecialization: undefined, disease: undefined });
    dataLayer.push({
        event: "select_item_with_filter",
        ecommerce: {
            items: [item]
        },
        activeFilters: getActiveFilters()
    });
}

//------------------------------ init doctor click event on "a tag"
function InitPlpSelectItem() {
    $(".rowItem_LC a").on("pointerdown", function (event) {
        //get parent of item " a tag  " 
        var itemClicked = $(this).parents(".rowItem_LC");

        switch (event.which) {
            case 1:
                PushPlpSelectItemData(itemClicked);
                break;
            case 3:
                //for right click
                break;
        }

    })

}

function InitPlpDrSuggestionViewItem() {
    const targetNode = document.querySelector('.jrny-modal-doctorSuggestion-body-dr-card')
    var observer = new MutationObserver(function (mutations) {
        var target = $('.jrny-modal-doctorSuggestion-body-dr-card');
        PushViewPlpDrSuggestionData(target)
    });

    observer.observe(targetNode, {
        attributes: true
    });

}

function PushViewPlpDrSuggestionData(target) {

    var subCategory = getUrlInfo().subCategory
    var categoryPlusSubCategoryCaption = $("#hidden-ecm-category-id").attr("data-cat-caption");
    //get doctor object from html tag
    var item = getPlpItemData(target)
    var doctorExpertise = $(target).attr('data-category');
    item.index = 0
    item.item_list_id = EItemListInfo['consultation_dr_suggestion_plp'].item_list_id + '_' + subCategory;
    item.item_list_name = EItemListInfo['consultation_dr_suggestion_plp'].item_list_name + categoryPlusSubCategoryCaption;
    item.item_category = doctorExpertise;
    item.item_category2 = '';

    dataLayer.push({ ecommerce: null });
    dataLayer.push({
        event: "view_item_list",
        ecommerce: {
            items: [item]
        }
    });
}

function PushSelectPlpDrSuggestionData(target) {

    var subCategory = getUrlInfo().subCategory
    var categoryPlusSubCategoryCaption = $("#hidden-ecm-category-id").attr("data-cat-caption");
    //get doctor object from html tag
    var item = getPlpItemData(target)
    var doctorExpertise = $(target).attr('data-category');
    item.index = 0
    item.item_list_id = EItemListInfo['consultation_dr_suggestion_plp'].item_list_id + '_' + subCategory;
    item.item_list_name = EItemListInfo['consultation_dr_suggestion_plp'].item_list_name + categoryPlusSubCategoryCaption;
    item.item_category = doctorExpertise;
    item.item_category2 = '';

    dataLayer.push({ ecommerce: null });
    dataLayer.push({
        event: "select_item",
        ecommerce: {
            items: [item]
        }
    });
}

function InitPlpDrSuggestionSelectItem() {
    $("a#jrny-category-suggest-dr-modal-start-consultation").on("pointerdown", function (event) {

        //get parent of item " a tag  " 
        var itemClicked = $('.jrny-modal-doctorSuggestion-body-dr-card');

        switch (event.which) {
            case 1:
            case 2:
                //for click 
                PushSelectPlpDrSuggestionData(itemClicked);
                break;
            case 3:
                //for right click
                break;
        }

    })

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

function getUrlInfo() {
    // get all applied filtered
    var filter = queryStringToJSON(window.location.href)

    // get sub Category
    var subCategory = window.location.pathname.split('/')
    subCategory = subCategory[subCategory.length - 1]
    
    return {
        subCategory, filter
    }
}