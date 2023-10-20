
$(document).ready(function () {

    InitEnhancedEcommercePromotionsView();
    InitEnhancedEcommercePromotionsClick();
})

//------------------------------ 
function GetPromotionEcommerceObjectInfo(doctor_item_tag) {
    var promoObj = {};

    promoObj["id"] = doctor_item_tag.attr("promo-id");
    promoObj["name"] = doctor_item_tag.attr("promo-name");
    promoObj["creative"] = doctor_item_tag.attr("promo-creative");
    promoObj["position"] = doctor_item_tag.attr("promo-position");;
    return promoObj;
}
//-----------------------------push data to from datalayer of google tag manager
function PushDataPromotionsViewToEnhancedEcommerce(promo_item_tag, pos) {

    //get  doctor object from html tag
    var promoObj = GetPromotionEcommerceObjectInfo(promo_item_tag);

    dataLayer.push({ ecommerce: null });
    dataLayer.push({
        'event': 'eec.promotionView',
        'ecommerce': {
            'promoView': {
                'promotions': [
                    {
                        'id': promoObj.id,
                        'name': promoObj.name,
                        'creative': promoObj.creative,
                        'position': promoObj.position
                    }
                ]
            }
        }
    });

    console.log(" promo View : ", promoObj);

}
//-------------------------------Get Data From "flickity slider"
function GetDataPromotionFromSlider(doctorSliderObject) {

    // check slider is available
    var bannerDocSlider = doctorSliderObject.data('flickity');

    if (bannerDocSlider == undefined) {
        console.log(" the flickity slider not found");
        return;
    }

    //get last slide cells
    var countPreSlidesCell = 0;
    for (var i = 0; i < bannerDocSlider.selectedIndex; i++) {

        countPreSlidesCell = countPreSlidesCell + bannerDocSlider.slides[i].cells.length;
    }

    // get selected Cells (doctor) in  slider
    for (var i = 0; i < bannerDocSlider.selectedCells.length; i++) {
        var docCell = $(bannerDocSlider.selectedCells[i].element);

        //check is before viewed
        if (docCell.attr("data-ecm-view") == "1")
            continue;
        docCell.attr("data-ecm-view", "1");

        //calculate doctor item postion in slider 
        var position = i + countPreSlidesCell;

        PushDataPromotionsViewToEnhancedEcommerce(docCell, position);
    }

    // init Slider Change Event
    if (doctorSliderObject.attr("data-slider-change-event") == "1")
        return;
    doctorSliderObject.attr("data-slider-change-event", "1");
    doctorSliderObject.on('change.flickity', function (event, index) {
        GetDataPromotionFromSlider(doctorSliderObject);
    });



}

//------------------------- Init Enhanced Ecommerce Promotions View
function InitEnhancedEcommercePromotionsView() {

    //check  waypoint library is available
    if ($('.promotions-enh-list').waypoint == undefined) {
        console.log(" the waypointsd library not found");
        return;
    }

    // check when promotions list item viewed by user and get data
    var waypoints = $('.promotions-enh-list').waypoint(function (direction) {

        //push data to from datalayer of google tag manager
        //get data from slider
        GetDataPromotionFromSlider($(this.element));

    }, {
        offset: '75%'
    })
}


//-----------------------------Get postistion Of doctor that clicked

function GetPositionOfDoctorInBannerClicked(sliderOfDoctorList, itemClicked) {

    // check slider is available
    var docSlider = sliderOfDoctorList.data('flickity');
    if (docSlider == undefined) {
        console.log(" the flickity slider not found");
        return;
    }

    //get last slide cells
    var countPreSlidesCell = 0;
    for (var i = 0; i < docSlider.selectedIndex; i++) {

        countPreSlidesCell = countPreSlidesCell + docSlider.slides[i].cells.length;
    }

    // get selected Cells (doctor) in  slider
    for (i = 0; i < docSlider.selectedCells.length; i++) {
        var docCell = $(docSlider.selectedCells[i].element);
        //check is before viewed
        if (docCell[0] == itemClicked[0]) {

            //calculate doctor item postion in slider 
            var position = i + countPreSlidesCell;
            return position
        }
    }
    return 0;
}

//-------------------------------Push Data Click Of  Doctor List In Banner Page
function PushDataClickOfDoctorListInBanner(promotionClickedObject) {

    //get  promotion object from html tag
    var promoObj = GetPromotionEcommerceObjectInfo(promotionClickedObject);

    dataLayer.push({ ecommerce: null });
    dataLayer.push({
        'event': 'eec.promotionClick',
        'ecommerce': {
            'promoClick': {
                'promotions': [
                    {
                        'id': promoObj.id,                         // Name or ID is required.
                        'name': promoObj.name,
                        'creative': promoObj.creative,
                        'position': promoObj.position
                    }]
            }
        }
    });
    console.log("Click : ", promoObj);
}

//------------------------------ init promotions click event
function InitEnhancedEcommercePromotionsClick() {

    $(".promotions-enh-list div[data-promo='true']").on("click",
        function(event) {

            //get parent of item " a tag  " 
            var itemClicked = $(this);
            PushDataClickOfDoctorListInBanner(itemClicked);

        });
}