const express=require('express');
const passport=require('passport');
const {errorNotCaught,errorNotFound}=require('./api/middleware/error');
const cors=require('cors');
const mongoose=require('mongoose')
const app=express();


// Connect to the database
const databaseString = `mongodb://localhost:27017/${process.env.DB_NAME}`;
mongoose.connect(databaseString, {
   useNewUrlParser: true,
   useUnifiedTopology: true
});

mongoose.connection.once('open', function(){
    console.log('Connection successful!');
});

mongoose.connection.on('error', error => {
    console.log('Error: ', error);
});


app.use(express.json());
app.use(express.urlencoded({extended:false}));
app.use(cors({origin:true,credentials:true}));
app.use(passport.initialize());


//routes

app.use("/api/img",express.static('resources/img'));

app.use(errorNotFound);
app.use(errorNotCaught);

module.exports=app;
