#!/bin/bash

#=================签名参数===============
#从xcconfig文件中取值
#解决Error Domain=IDEDistributionErrorDomain Code=14 "No applicable devices found."
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"
rvm use system
xcodebuild "$@"

#=================项目路径配置===============
PROJECT_PATH='/Users/hc/Desktop/Me/MultipleChannel'
WORKSPACE_NAME='MultipleChannel.xcworkspace'
Archive_PATH='/Users/hc/Desktop/Archive'
IPA_PATH='/Users/hc/Desktop/Ipa'
EXPORT_PLIST_PATH='/Users/hc/Desktop/Me/MultipleChannel/exportArchive.plist'


#===================================脚本开始=================================================
#使用帮助
if [ $# == 0 ];then
echo "===========================如何使用============================="
echo " eg: ./build [scheme] [token] '版本描述中间不要留空格', 不传token默认用当前已经登录的fir token"
echo "================================================================"
exit
fi

#update code from gitlab
cd $PROJECT_PATH
#git pull

#update pod
pod install --repo-update
pod update

#删除旧的编译目录
APP_BUILD_LOCATION=${PROJECT_PATH}/Build/
rm -rf ${APP_BUILD_LOCATION}
#创建dfc目录

#key auth
#security unlock-keychain "-p" "123456" "/Users/hc/Library/Keychains/login.keychain"

#创建ARCHIVE目录
mkdir -p IPA_PATH

#开始打包
cd ${PROJECT_PATH}
pwd

XCCONFIG_PATH=${PROJECT_PATH}/dfc_v2/appconfig
xcodebuild -workspace ${WORKSPACE_NAME} -scheme $1 -config $1 -archivePath ${Archive_PATH}/$1.xcarchive archive

#创建ipa
IPA_LOCATION=${IPA_PATH}/$1
#删除旧的ipa
rm -rf IPA_LOCATION
mkdir -p ${IPA_PATH}/$1
xcodebuild -exportArchive -exportOptionsPlist ${EXPORT_PLIST_PATH} -archivePath ${Archive_PATH}/$1.xcarchive -exportPath ${IPA_LOCATION}

IPA_FILE_LOCATION=${IPA_PATH}/$1/$1.ipa

#检查ipa是否创建成功
if [ -f $IPA_FILE_LOCATION ]; then
echo "ipa已经创建:"${IPA_FILE_LOCATION}
else
echo "打包失败"
exit 0
fi


#上传
if [ $# -ge 2 ];then
fir p ${IPA_FILE_LOCATION} -T $2
else
echo "请填写fir-token上传"
fi
