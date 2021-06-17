const errorNotFound=(req,res,next)=>{
    const error=new Error("Not found")
    error.status=404
    next(error)
}
const errorNotCaught=(error,req,res,next)=> {
    res.status(error.status ?? 500)
    if(process.env.NODE_ENV==='development')
        return res.json({
            message:error.message,
            stack:error.stack
        })
    return res.json({
        message:error.message
    })
}

module.exports = {errorNotFound,errorNotCaught}
