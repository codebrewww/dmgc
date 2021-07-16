let td_sum_cal, td_sum_carb, td_sum_pro , td_sum_fat;

window.addEventListener("load", function(event) {
    td_sum_cal = document.getElementById("td-sum-cal");
    td_sum_carb = document.getElementById("td-sum-carb");
    td_sum_pro = document.getElementById("td-sum-pro");
    td_sum_fat = document.getElementById("td-sum-fat");

    td_sum_cal.innerHTML=0;
    td_sum_carb.innerHTML=0;
    td_sum_pro.innerHTML=0;
    td_sum_fat.innerHTML=0;
});

function calc(e){
    // 칼로리
    let tempCal = Number(td_sum_cal.innerText);
    const cal = Number(e.target.dataset.cal);

    if(e.target.checked) {
        tempCal = tempCal + cal;
    } else {
        tempCal = tempCal - cal;
    }
    td_sum_cal.innerText = Math.floor(tempCal);

    // 탄수화물
    const td_sum_carb_arr = td_sum_carb.innerText.split('(');
    console.log(td_sum_carb_arr)

    let tempCarb = Number(td_sum_carb_arr[0]);
    const carb = Number(e.target.dataset.carb);

    let tempSugar = 0;
    if(td_sum_carb_arr.length>1) {
        tempSugar = Number(td_sum_carb_arr[1].split(')')[0]);
        console.log(tempSugar)
    }
    const sugar = Number(e.target.dataset.sugar);

    if(e.target.checked) {
        tempCarb = tempCarb + carb;
        tempSugar = tempSugar + sugar;
    } else {
        tempCarb = tempCarb - carb;
        tempSugar = tempSugar - sugar;
    }

    td_sum_carb.innerText = `${Math.floor(tempCarb)}(${Math.floor(tempSugar)})`;

    // 단백질
    let tempPro = Number(td_sum_pro.innerText);
    const pro = Number(e.target.dataset.pro);

    if(e.target.checked) {
        tempPro = tempPro + pro;
    } else {
        tempPro = tempPro - pro;
    }
    td_sum_pro.innerText = Math.floor(tempPro);

    // 지방(불포화)
    const td_sum_fat_arr = td_sum_fat.innerText.split('(');
    console.log(td_sum_fat_arr)

    let tempFat = Number(td_sum_fat_arr[0]);
    const fat = Number(e.target.dataset.fat);

    let tempUnfat = 0;
    if(td_sum_fat_arr.length>1) {
        tempUnfat = Number(td_sum_fat_arr[1].split(')')[0]);
        console.log(tempUnfat)
    }
    const unfat = Number(e.target.dataset.unfat);

    if(e.target.checked) {
        tempFat = tempFat + fat;
        tempUnfat = tempUnfat + unfat;
    } else {
        tempFat = tempFat - fat;
        tempUnfat = tempUnfat - unfat;
    }

    td_sum_fat.innerText = `${Math.floor(tempFat)}(${Math.floor(tempUnfat)})`;
}

const onChangeFoodSize = (e) => {
    console.log(e.target.value)
}