$(function() {
    let initTellerBalance = getTellerBalance(); //Teller Balance from server
    let initBalanceFormArray = getTellerBalanceForm(); //Balance form from server
    newBalance = calculateTellerBalance(initBalanceFormArray, initTellerBalance);

    $('.balanceFormField').change(function () {
        let balanceFormArray =  getTellerBalanceForm() 
        let newBalance = calculateTellerBalance(balanceFormArray, initTellerBalance)
        $('#tellerBalance').html(newBalance);
        
    });
    
    function createNewBalanceEntry (elementId, elementValue) {
        elementValueFlt = htmlToFloat(elementValue)

        let newEntry = {
            elementId : elementId,
            elementValue : elementValue,
            elementFloat : elementValueFlt
        };
        return newEntry
    };


    function getTellerBalanceForm() {   //moves through each element and logs value as an array of objects
        balanceFormArray = []
        $('.balanceFormField').each( function (indexInArray, valueOfElement) {
            let elementId = $(this).attr('id');
            let elementValue = $(this).val();
            if (['0', ''].includes((elementValue).trim())) {   //checks for empty form and fills with zeros
                elementValue = '0.00'
                $(this).val(elementValue)
            };
            if (!elementValue.includes('.')){
                elementValue = elementValue + '.00'
                $(this).val(elementValue)
            };
            let balanceFormEntry = createNewBalanceEntry(elementId, elementValue);

            balanceFormArray.push(balanceFormEntry);
        });//end for loop
        return balanceFormArray
    };

    function calculateTellerBalance(formArray, initTellerBalance){ //initTellerBalance used so calculations are absolute.
        let totalBalanced
        for (let index = 0; index < formArray.length; index++) {
            const elementObj = formArray[index];
            if ( index < 1) {
                totalBalanced = elementObj.elementFloat
            } else {
                totalBalanced = totalBalanced +elementObj.elementFloat
            }
        }//end for loop
        let newTellerBalanceFlt = initTellerBalance.floatBalance - totalBalanced
        return newTellerBalanceFlt
    }; //end calcTellerBalance

    function getTellerBalance(){
        let currentTellerCashStrVal = $('#tellerBalance').html();
        let currentTellerCashFltVal = htmlToFloat(currentTellerCashStrVal);
        tellerBalance = createTellerBalance(currentTellerCashFltVal, currentTellerCashStrVal);

        return tellerBalance

    };  //end teller balance constructor

    function createTellerBalance (floatBalance, stringBalance) {
        let newTellerBalance = {
            floatBalance : floatBalance,
            stringBalance : stringBalance
        };
        return newTellerBalance
    };

    function htmlToFloat(htmlValue){
        htmlValue = htmlValue.replace('$', '');  //removes $ from str
        htmlValue = htmlValue.replace(',', ''); //removes comma so formatted str wont return leading 2 numbers
        htmlValue = htmlValue.trim();   //removes whitespace for float formatting
        htmlValue = parseFloat(htmlValue);
        return htmlValue
    }

}); //close doc ready statement
