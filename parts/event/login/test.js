/*
 * Copyright (c) 2025 UF4OVER
 *  All rights reserved.
 */

if (navigator.sharedCredentials) //浏览器是否支持Keyring
{
    navigator.sharedCredentials.isSupported().then((supported)=>{
        //HMS Core是否支持Keyring
        console.info("SharedCredentials isSupported : " + supported);
    }, (err) => {
        console.error("SharedCredentials Error: ", err);
    });
}
else
{
    console.info("SharedCredentials is not supported on HuaweiBrowser");
}