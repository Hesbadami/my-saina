$(document).ready(function () {
    $(document).on('change', '.consultation-filter-input', function() {
        ecommerceFiltersClickHandler(this.id, this.checked)
    });
});

var plans = {
    FastPhoneCall: 'FastPhoneCall',
    PhoneCall : 'PhoneCall',
    VideoPhoneCall : 'VideoPhoneCall',
    Text : 'Text'
}

var gender = {
    male: 'male',
    female: 'female'
}
var searchPagePlans = {
    4: 'FastPhoneCall',
    2 : 'PhoneCall',
    5 : 'VideoPhoneCall',
    1 : 'Text'
}

var searchPageGender = {
    0: 'male',
    1: 'female'
}

function ecommerceFiltersClickHandler(elementId, value) {
    switch (elementId) {
        case 'cb_isOnline':
            ecommerceFiltersEventEmitter({
                isOnline: true
            }, value)
            break;
        case 'cb_hasInsurance':
            ecommerceFiltersEventEmitter({
                hasInsurance: true
            }, value)
            break;
        case 'cb_hasFastPhoneCall':
            ecommerceFiltersEventEmitter({
                activePlan: plans.FastPhoneCall
            }, value)
            break;
        case 'cb_hasPhoneCall':
            ecommerceFiltersEventEmitter({
                activePlan: plans.PhoneCall
            }, value)
            break;
        case 'cb_hasVideoCall':
            ecommerceFiltersEventEmitter({
                activePlan: plans.VideoPhoneCall
            }, value)
            break;
        case 'cb_hasChat':
            ecommerceFiltersEventEmitter({
                activePlan: plans.Text
            }, value)
            break;
        case 'justFemaleR':
            ecommerceFiltersEventEmitter({
                gender: gender.female
            }, value)
            break;
        case 'justMaleR':
            ecommerceFiltersEventEmitter({
                gender: gender.male
            }, value)
            break;
        case 'f_specialization':
        case 'f_specialization_0':
            ecommerceFiltersEventEmitter({
                specialization: true
            }, value)
            break;
        case 'f_upper_specialization':
        case 'f_specialization_1':
            ecommerceFiltersEventEmitter({
                upperSpecialization: true
            }, value)
            break;
        case 'disease':
            var diseaseId = getActiveFilterValue('disease');
            ecommerceFiltersEventEmitter({
                disease: diseaseId
            }, value)
            break;
    }
}

function ecommerceFiltersEventEmitter(data, value) {
    // window.dataLayer = window.dataLayer.filter(item => item.event !== 'add_filter').filter(item => item.event !== 'remove_filter') || [];
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ecommerce: undefined, activePlan: undefined, gender: undefined, hasInsurance: undefined, isOnline: undefined, specialization: undefined, upperSpecialization: undefined, disease: undefined})
    window.dataLayer.push({
        event: value === true ? 'add_filter' : 'remove_filter',
        ...data
    });
}

function getActiveFilters() {
    var activePlans = []
    var genderArr = [];
    getActiveFilter('cb_hasPhoneCall') && activePlans.push(plans.PhoneCall);
    getActiveFilter('cb_hasFastPhoneCall') && activePlans.push(plans.FastPhoneCall);
    getActiveFilter('cb_hasVideoCall') && activePlans.push(plans.VideoPhoneCall);
    getActiveFilter('cb_hasChat') && activePlans.push(plans.Text);
    getActiveFilter('justFemaleR') === true && genderArr.push(gender.female)
    getActiveFilter('justMaleR') === true && genderArr.push(gender.male)
    return {
        ...(activePlans.length > 0 ? {activePlans: activePlans} : null),
        ...(getActiveFilter('cb_hasInsurance') ? {hasInsurance: true} : null),
        ...(genderArr.length > 0 ? {gender: genderArr} : null),
        ...(getActiveFilter('cb_isOnline') ? {isOnline: true} : null),
        ...(getActiveFilter('f_specialization') ? {specialization: true} : null),
        ...(getActiveFilter('f_upper_specialization') ? {upperSpecialization:  true} : null),
        ...(getActiveFilter('disease') ? {disease:  getActiveFilterValue('disease')} : null),
    }
}

function getActiveFiltersForSearchPage() {
    var activePlans = []
    getActiveFilter('cb_hasPhoneCall') && activePlans.push(plans.PhoneCall);
    getActiveFilter('cb_hasFastPhoneCall') && activePlans.push(plans.FastPhoneCall);
    getActiveFilter('cb_hasVideoCall') && activePlans.push(plans.VideoPhoneCall);
    getActiveFilter('cb_hasChat') && activePlans.push(plans.Text);
    
    return {
        ...(getActiveFilter('ActivePlan') ? {activePlans: getActiveFilterValue('ActivePlan').split('#').map(item => searchPagePlans[item])} : null),
        ...(getActiveFilter('ActiveInsurance') ? {hasInsurance: true} : null),
        ...(getActiveFilter('Gender') === true ? {gender : searchPageGender[getActiveFilterValue('Gender')]} : null),
        ...(getActiveFilter('isOnline') ? {isOnline: true} : null),
        ...(getActiveFilter('SuperExpert') ? getActiveFilterValue('SuperExpert') === 'true' ? {upperSpecialization:  true} : {specialization: true} : null),
    }
}

function getActiveFilter(filterSlug) {
    var url = new URL(window.location.href);
    var params = new URLSearchParams(url.search);
    return !!params.get(filterSlug)
}

function getActiveFilterValue(filterSlug) {
    var url = new URL(window.location.href);
    var params = new URLSearchParams(url.search);
    return params.get(filterSlug)
}

function onClickDiseaseFilter(hasHref = false, diseaseId) {
    var extractedDiseaseId = hasHref ? diseaseId : getActiveFilterValue('disease')
    ecommerceFiltersEventEmitter({
        disease: extractedDiseaseId
    }, hasHref)
}