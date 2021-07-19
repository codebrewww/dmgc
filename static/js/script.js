let td_sum_cal, td_sum_carb, td_sum_pro , td_sum_fat;

window.addEventListener("load", function(event) {
    td_sum_cal = document.getElementById("td-sum-cal");
    td_sum_carb = document.getElementById("td-sum-carb");
    td_sum_sugar = document.getElementById("td-sum-sugar");
    td_sum_pro = document.getElementById("td-sum-pro");
    td_sum_fat = document.getElementById("td-sum-fat");
    td_sum_unfat = document.getElementById("td-sum-unfat");

    td_sum_cal.innerText=0;
    td_sum_carb.innerText=0;
    td_sum_sugar.innerText=0;
    td_sum_pro.innerText=0;
    td_sum_fat.innerText=0;
    td_sum_unfat.innerText=0;
});

function calc(e){
    // 칼로리
    let tempCal = Number(td_sum_cal.innerText);
    const cal = Number(e.target.dataset.cal);

    // 탄수화물
    let tempCarb = Number(td_sum_carb.innerText);
    const carb = Number(e.target.dataset.carb);

    let tempSugar = Number(td_sum_sugar.innerText);
    const sugar = Number(e.target.dataset.sugar);

    // 단백질
    let tempPro = Number(td_sum_pro.innerText);
    const pro = Number(e.target.dataset.pro);

    //지방
    let tempFat = Number(td_sum_fat.innerText);
    const fat = Number(e.target.dataset.fat);

    let tempUnfat = Number(td_sum_unfat.innerText);
    const unfat = Number(e.target.dataset.unfat);

    if(e.target.checked) {
        tempCal = tempCal + cal;
        tempCarb = tempCarb + carb;
        tempSugar = tempSugar + sugar;
        tempPro = tempPro + pro;
        tempFat = tempFat + fat;
        tempUnfat = tempUnfat + unfat;
    } else {
        tempCal = tempCal - cal;
        tempCarb = tempCarb - carb;
        tempSugar = tempSugar - sugar;
        tempPro = tempPro - pro;
        tempFat = tempFat - fat;
        tempUnfat = tempUnfat - unfat;
    }

    td_sum_cal.innerText = Math.floor(tempCal) < 0 ? 0 : Math.floor(tempCal) ;
    td_sum_carb.innerText = Math.floor(tempCarb)<0? 0: Math.floor(tempCarb);
    td_sum_sugar.innerText= Math.floor(tempSugar)<0? 0:Math.floor(tempSugar);
    td_sum_pro.innerText = Math.floor(tempPro)<0?0:Math.floor(tempPro);
    td_sum_fat.innerText = Math.floor(tempFat)<0?0:Math.floor(tempFat);
    td_sum_unfat.innerText = Math.floor(tempUnfat)<0?0:Math.floor(tempUnfat);
}

const onChangeFoodSize = (e) => {
    const el_selected = e.target;
    const ele_tr = el_selected.closest('tr');
    const ele_tr_childs = ele_tr.getElementsByClassName("checkbox-nutr")[0].dataset;

    const originalValue = Number(ele_tr_childs['orgfoodsize']);

    // 제공횟수 변경되도록
    const changedValue = e.target.value/originalValue;
    const ele_foodamount = ele_tr.getElementsByClassName('input-nutr-foodamount')[0];
    ele_foodamount.value = changedValue;


    onChangeFood(e, e.target.value, originalValue);
}

const onChangeFoodAmount = (e) => {
    // onChangeFood(e, 1.0);
    const el_selected = e.target;
    const ele_tr = el_selected.closest('tr');
    const ele_tr_childs = ele_tr.getElementsByClassName("checkbox-nutr")[0].dataset;


    const changedValue =  ele_tr_childs['orgfoodsize'] * el_selected.value;

    // 제공량 변경되도록
    const ele_foodsize = ele_tr.getElementsByClassName('input-nutr-foodsize')[0];
    ele_foodsize.value = changedValue;


    const originalValue = Number(ele_tr_childs['orgfoodsize']);

    onChangeFood(e, changedValue, originalValue);
}

const onChangeFood = (e, changedValue, originalValue) => {
    const el_selected = e.target;
    // const changedValue = e.target.value;

    const ele_tr = el_selected.closest('tr');
    // 체크 되어 있을 경우 해제
    const ele_tr_check = ele_tr.getElementsByClassName('checkbox-nutr')[0];
    if(ele_tr_check.checked) {
        ele_tr_check.click();
    }

    const ele_tr_childs = ele_tr.getElementsByClassName("checkbox-nutr")[0].dataset;

    const ratio = changedValue/originalValue;

    const el_cal = ele_tr.getElementsByClassName('td-nutr-cal')[0];
    const changedCal = Math.floor( ele_tr_childs['orgcal'] * ratio);
    ele_tr_childs['cal']  = changedCal;
    el_cal.innerText = changedCal;

    // 탄수화물
    const el_carb = ele_tr.getElementsByClassName('td-nutr-carb')[0];
    el_carb.innerText = String(Math.floor(ele_tr_childs['orgcarb'] * ratio));

    // 당류
    const el_sugar = ele_tr.getElementsByClassName('td-nutr-sugar')[0];
    el_sugar.innerText = String(Math.floor(ele_tr_childs['orgsugar'] * ratio));

    // 단백질
    const el_pro = ele_tr.getElementsByClassName('td-nutr-pro')[0];
    el_pro.innerText = String(Math.floor(ele_tr_childs['orgpro'] * ratio));

    // 지방
    const el_fat = ele_tr.getElementsByClassName('td-nutr-fat')[0];
    el_fat.innerText = String(Math.floor(ele_tr_childs['orgfat'] * ratio));

    // 불포화지방
    const el_unfat = ele_tr.getElementsByClassName('td-nutr-unfat')[0];
    el_unfat.innerText = String(Math.floor(ele_tr_childs['orgunfat'] * ratio));
}