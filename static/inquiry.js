$(function() { 
    let accountBalance = document.getElementById('accountBalance');
    let accountBalanceStr = (accountBalance).innerHTML;
    let accountBalanceFlt = htmlToFloat(accountBalanceStr); 
    checkBalancePositive(accountBalanceFlt, accountBalance)
    let elementArray = makeElementArray()
    let newElementArray = calculateRunningBalance(elementArray, accountBalanceFlt);
    addRunningBalance(newElementArray)
    

    function htmlToFloat(htmlValue){
        htmlValue = (htmlValue).replace('$', '');  //removes $ from str
        htmlValue = htmlValue.replace(/,/g, ''); //removes comma so formatted str wont return leading 2 numbers
        htmlValue = htmlValue.replace('(', '-');
        htmlValue = htmlValue.replace(')', '');
        htmlValue = htmlValue.trim();   //removes whitespace for float formatting
        htmlValue = parseFloat(htmlValue);
        return htmlValue
    };

    function makeTransObj(transaction, creditOrDebit, runningBalance = 0){
        let newObj = {
            transactionValue : transaction,
            creditOrDebit : creditOrDebit,
            runningBalance : runningBalance
        };
        return newObj
    };

    function makeElementArray(){
        let elementArray = []
        $('.trans').each(function (index, element) {
            // element == this
            if ($(this).attr('data-dir') == 'debit'){
                let debit = 'debit'
                let transFlt = htmlToFloat((this).innerHTML)
                let transObj = makeTransObj(transFlt, debit)
                elementArray.push(transObj)

            } else if ($(this).attr('data-dir') == 'credit'){
                let credit = 'credit'
                let transFlt = htmlToFloat((this).innerHTML)
                let transObj = makeTransObj(transFlt,credit)
                elementArray.push(transObj)

            };
        });
        return elementArray
    };

    function calculateRunningBalance(elementArray, accountBalanceFlt){
        let newArray = []
        array = elementArray.reverse()
        for (let index = 0; index < array.length; index++) {
            const element = array[index];
            element.runningBalance = accountBalanceFlt.toFixed(2)
            accountBalanceFlt = accountBalanceFlt - element.transactionValue
            newArray.push(element)
        };
        return newArray
    };

    function addRunningBalance(newElementArray){
        $('.runningBalance').each(function (index, element) {
            // element == this
            transObj = newElementArray.pop()
            let runningBalance = formatRunningBalance(transObj.runningBalance);
            $(this).html(runningBalance)
            if (runningBalance.includes('(')){
                (this).setAttribute('data-dir', 'debit')    
            };
        });
    };

    function formatRunningBalance(runningBalance){
        runningBalance = parseFloat(runningBalance)
        if (runningBalance > 0){
            runningBalance = (runningBalance.toFixed(2)).replace(/\d(?=(\d{3})+\.)/g, '$&,');
            runningBalance = '$' + runningBalance
        } else if (runningBalance < 0 ){
            runningBalance = (runningBalance.toFixed(2)).replace(/\d(?=(\d{3})+\.)/g, '$&,');
            runningBalance = runningBalance.replace('-','')
            runningBalance = '($' + runningBalance + ')'
        } else {
            runningBalance.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
            runningBalance = '$' + runningBalance
        };
        return runningBalance
    };

    function checkBalancePositive (accountBalanceFlt, accountBalance) {
        if (accountBalanceFlt < 0) {
            (accountBalance).setAttribute('data-dir', 'debit')
        };
    };

});