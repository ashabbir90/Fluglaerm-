//JSON Time Angaben deserialisiern
/*
    run in terminal
    "> node make_dates_readable.js" 

*/
console.log("---------- Datumsangabe deserailisiert----------")


const fs = require ('fs');


//.....read local json file
fs.readFile('./data_cut.json','utf-8', (err, myData) => {
  if (err){
    console.log(err);
  } else {
   
 //.....JSON-Manipulation                                                       
data = JSON.parse(myData);
 
                                                    
data = data.map((item)=>({
  ...item,
  STA : new Date (item.STA), // some Value -1 == 1969,.... 
  STD : new Date (item.STD), // some Value -1 == 1969,....
  Time: new Date (item.Time),
  ATA : new Date (item.ATA),
  ATD : new Date (item.ATD)

}))
        
    //......Write new File
    fs.writeFile('./cut_data_deserialized.json', JSON.stringify(data, null, 2), 'utf-8', err =>{
      if(err) {
        console.log(err);
      }
    });
  }
});



