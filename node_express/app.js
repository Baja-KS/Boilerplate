const express=require('express');
const passport=require('passport');
const {errorNotCaught,errorNotFound}=require('./api/middleware/error');
const cors=require('cors');

const app=express();

const {sequelize}=require('./models/index');


sequelize.authenticate().then(()=>console.log("DB Connection Successful")).catch(()=>console.log("DB connection failed"))

app.use(express.json());
app.use(express.urlencoded({extended:false}));
app.use(cors({origin:true,credentials:true}));
app.use(passport.initialize());


//routes

app.use("/api/img",express.static('resources/img'));

app.use(errorNotFound);
app.use(errorNotCaught);

module.exports=app;
