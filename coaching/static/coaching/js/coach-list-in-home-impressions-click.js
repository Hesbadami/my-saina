
var bestDoctorSliderChangeEvent = false;

$(document).ready(function () {

    InitBestDoctorsInHomeIpressions();
    InitBestDoctorsInHomeClickEvent();

})

//------------------------------ 
function GetDoctorCatEcommerceInfoForIpressionsEvent(doctor_item_tag, pos) {
    var docObj = {};

    docObj["id"] = doctor_item_tag.attr("data-id");
    docObj["name"] = doctor_item_tag.attr("data-name");
    docObj["category"] = doctor_item_tag.attr("data-category");
    docObj["position"] = pos;
    docObj["list"] = "best-doctors-home";
    return docObj;
}
//-----------------------------push data to from datalayer of google tag manager
function PushDataIpressionsOfBestDoctorListInHome(doctor_item_tag, pos) {

    //get  doctor object from html tag
    var docObj = GetDoctorCatEcommerceInfoForIpressionsEvent(doctor_item_tag, pos);
    dataLayer.push({ ecommerce: null });
    dataLayer.push({
        'event': 'eec.productImpression',
        'ecommerce': {
            'impressions': [
                {
                    'name': docObj.name,
                    'id': docObj.id,
                    'category': docObj.category,
                    'list': docObj.list,
                    'position': docObj.position
                }]
        }
    });
    //console.log("View : ", docObj);
}
//-------------------------------Get Data From "flickity slider"
function GetDataBestDoctorHomeFromSlider() {

    // check slider is available
    var bestDocSlider = $("#best-doctor .doctor-list").data('flickity');
    if (bestDocSlider == undefined) {
        console.log(" the flickity slider not found");
        return;
    }

    //get last slide cells
    var countPreSlidesCell = 0;
    for (var i = 0; i < bestDocSlider.selectedIndex; i++) {

        countPreSlidesCell = countPreSlidesCell + bestDocSlider.slides[i].cells.length;
    }

    // get selected Cells (doctor) in  slider
    for (i = 0; i < bestDocSlider.selectedCells.length; i++) {
        var docCell = $(bestDocSlider.selectedCells[i].element);
        //check is before viewed
        if (docCell.attr("data-ecm-view") == "1")
            continue;
        docCell.attr("data-ecm-view", "1");

        //calculate doctor item postion in slider 
        var position = i + countPreSlidesCell;

        PushDataIpressionsOfBestDoctorListInHome(docCell, position);
    }

    // init Slider Change Event
    if (bestDoctorSliderChangeEvent == true)
        return;
    bestDoctorSliderChangeEvent = true;
    $("#best-doctor .doctor-list").on('change.flickity', function (event, index) {
        GetDataBestDoctorHomeFromSlider();
    });



}


//------------------------------ Init Doctors In Home Page Ipressions
function InitBestDoctorsInHomeIpressions() {

    //check  waypoint library is available
    if ($('#best-doctor .doctor-list').waypoint == undefined) {
        console.log(" the waypointsd library not found");
        return;
    }

    // check when doctor item viwed by user and get data 
    var waypoints = $('#best-doctor .doctor-list').waypoint(function (direction) {

        //push data to from datalayer of google tag manager
        //get data from slider
        GetDataBestDoctorHomeFromSlider()
    }, {
        offset: '75%'
    })
}



//-----------------------------Get postistion Of doctor that clicked

function GetPositionOfDoctorClicked(itemClicked) {

    // check slider is available
    var bestDocSlider = $("#best-doctor .doctor-list").data('flickity');
    if (bestDocSlider == undefined) {
        console.log(" the flickity slider not found");
        return;
    }

    //get last slide cells
    var countPreSlidesCell = 0;
    for (var i = 0; i < bestDocSlider.selectedIndex; i++) {

        countPreSlidesCell = countPreSlidesCell + bestDocSlider.slides[i].cells.length;
    }

    // get selected Cells (doctor) in  slider
    for (i = 0; i < bestDocSlider.selectedCells.length; i++) {
        var docCell = $(bestDocSlider.selectedCells[i].element);
        //check is before viewed
        if (docCell[0] == itemClicked[0]) {

            //calculate doctor item postion in slider 
            var position = i + countPreSlidesCell;
            return position
        }
    }
    return 0;
}


function SaveDataForRightClickOfDoctorListInHome(productObj) {

    //get  doctor object from html tag
    var position = GetPositionOfDoctorClicked(productObj)

    //get  doctor object from html tag
    var docObj = GetDoctorCatEcommerceInfoForIpressionsEvent(productObj, position);

    SetEnanceEcommerceImpresionLog(docObj);

    //console.log("right Click : ", docObj);
}

//save last list of doctor that viewed 
function SetEnanceEcommerceImpresionLog(doctorObj) {
    var date = new Date();
    var minutes = 1;
    date.setTime(date.getTime() + (minutes * 60 * 1000));
    Cookies.set("lst" + doctorObj.id, doctorObj.list, { expires: date });
    Cookies.set("lst_pos_" + doctorObj.id, doctorObj.position, { expires: date });

}

//-------------------------------Push Data Click Of Best Doctor List In Home Page
function PushDataClickOfBestDoctorListInHome(productObj) {
    
    var position = GetPositionOfDoctorClicked(productObj)

    //get  doctor object from html tag
    var docObj = GetDoctorCatEcommerceInfoForIpressionsEvent(productObj, position);

    dataLayer.push({ ecommerce: null });
    dataLayer.push({
        'event': 'eec.productClick',
        'ecommerce': {
            'click': {
                'actionField': { 'list': docObj.list },
                'products': [{
                    'name': docObj.name,
                    'id': docObj.id,
                    'category': docObj.category,
                    'position': docObj.position
                }]
            }
        },
        //'eventCallback': function () {
        //    document.location = productObj.url
        //}
    });
    //console.log("Click : ", docObj);
}

//------------------------------ init doctor click event 
function InitBestDoctorsInHomeClickEvent() {
    var isTouchDevice = 'ontouchstart' in document.documentElement;

    $("#best-doctor .doctor-list .md-drsaina-btn," +
        "#best-doctor .doctor-list .doctor-img").on("pointerdown",function (event) {

            ///get parent of item " a tag  " 
            var itemClicked = $(this).parents(".flickity-spacing-doctor-list");

            switch (event.which) {
                case 1:
                    //for left click 
                    PushDataClickOfBestDoctorListInHome(itemClicked);

                    break;
                case 3:
                    //for right click
                    if (isTouchDevice == false)
                        SaveDataForRightClickOfDoctorListInHome(itemClicked);
                    break;
            }

        })

    // for mobile browser long touch for new tab  
    if (isTouchDevice) {
        $("#best-doctor .doctor-list .md-drsaina-btn," +
            "#best-doctor .doctor-list .doctor-img").on('touchstart', function () {

            //get parent of item " a tag  " 
            var itemClicked = $(this).parents(".flickity-spacing-doctor-list");
            var pressTimer = window.setTimeout(function () {

                SaveDataForRightClickOfDoctorListInHome(itemClicked);

            }, 300);
            $(this).on('touchend', function () {
                if (isTouchDevice) {

                    clearTimeout(pressTimer);
                }
            });

        });

    }

}


