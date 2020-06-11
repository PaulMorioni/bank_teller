$(function() {

    customer_attr_types = [['name', 'Name'], ['ssn', 'SSN']]
    account_attr_types = [['account_number', 'Account Number'], ['product', 'Product'], ['date_opened', 'Date Opened']]

    customerAttrObjs = attrObjFromArray(customer_attr_types);
    accountAttrObjs = attrObjFromArray(account_attr_types);

    attrTypeElement = document.getElementById('attrType')

    $('.searchType').click(function() { 
        let searchAttr
        let radioVal =
        $("input[name='searchType']:checked").attr('id');

        if (radioVal == 'searchType1') {
            searchAttr = customerAttrObjs;

        } else if (radioVal == 'searchType2') {
            searchAttr = accountAttrObjs;
        };
        let optionHTML
        for (let index = 0; index < searchAttr.length; index++) {
            const element = searchAttr[index];
            optionHTML += '<option value="' + element.value + '">' + element.text + '</option>';
            
        };

        attrTypeElement.innerHTML = optionHTML;

    });

    function makeAttrObj(value, text){
        let newObj =
        {
            value : value,
            text : text
        }
        return newObj
    };

    function attrObjFromArray(array) { 
        let objArray = []
        for (let index = 0; index < array.length; index++) {
            const element = array[index];
            let name = element[0]
            let value = element[1]

            let newObj = makeAttrObj(name, value);
            objArray.push(newObj);
        }
        return objArray
     };

}); //ends container function call