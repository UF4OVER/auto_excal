/*
 * Copyright (c) 2025 UF4OVER
 *  All rights reserved.
 */

if (navigator.sharedCredentials) //������Ƿ�֧��Keyring
{
    navigator.sharedCredentials.isSupported().then((supported)=>{
        //HMS Core�Ƿ�֧��Keyring
        console.info("SharedCredentials isSupported : " + supported);
    }, (err) => {
        console.error("SharedCredentials Error: ", err);
    });
}
else
{
    console.info("SharedCredentials is not supported on HuaweiBrowser");
}