# -*- coding: utf-8 -*-

import os;
import sys;
import getopt;

def setParameters():
	global Project_Path;
	global Workspace_Name;
	global Archive_Path;
	global Ipa_Path;
	global Plist_path;
	global Scheme;
	global FirToken;

	#工程的根目录
	Project_Path = '/Users/hc/Desktop/Me/MultipleChannel';
	#工程名
	Workspace_Name = 'MultipleChannel.xcworkspace';
	#生成Archive包的路径
	Archive_Path = '/Users/hc/Desktop/Archive';
	#生成的IPA包的路径
	Ipa_Path = '/Users/hc/Desktop/Ipa';
	#Xcode8.3后需要指定的plist文件的路径
	Plist_path = '%s/exportArchive.plist'%(Project_Path);
	
	if (len(sys.argv) != 3):
		print("************************************" + "\n" + "请使用这种格式运行脚本 python3 build.py [Scheme Name] [Fir Token]" + "\n" + "目前支持的Scheme有:  Develop  PrePublish  Enterprise" + "\n" + "************************************");
		os._exit(0);
	else:
		#Scheme, 需要传进来指定的Scheme名称
		Scheme = sys.argv[1];
		#Fir的Token 
		FirToken = sys.argv[2];
	return;

def deleteOldBuildFile():
	os.system("rm -rf %s/Build/"%(Project_Path));
	return;

def podUpdate():
	print("***************" + "%s"%(Project_Path));
	os.chdir("%s/"%(Project_Path))
	os.system("pwd");
	os.system("pod repo update");
	os.system("pod update --no-repo-update");
	return;

def createFinder():
	if not os.path.exists(Archive_Path):
		os.system("mkdir -p %s"%(Archive_Path));
	return;

def buildArchive():
	os.system("pwd");
	if os.path.exists("%s/%s.xcarchive"%(Archive_Path, Scheme)):
		print("********************************" + "%s/%s.xcarchive"%(Archive_Path, Scheme));
		os.system("rm -rf %s/%s.xcarchive"%(Archive_Path, Scheme));
	os.system("xcodebuild -workspace %s -scheme %s -config %s -archivePath %s/%s.xcarchive archive"%(Workspace_Name, Scheme, Scheme, Archive_Path, Scheme));
	return;

def importIpa():
	os.system("rm -rf %s/%s"%(Ipa_Path,Scheme));
	os.system("mkdir -p %s/%s"%(Ipa_Path,Scheme));
	if os.path.exists("%s/%s.ipa"%(Ipa_Path, Scheme)):
		os.system("rm -rf -p %s/%s.ipa"%(Ipa_Path, Scheme));
	os.system("xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s/%s -exportOptionsPlist %s"%(Archive_Path, Scheme, Ipa_Path, Scheme, Plist_path));
	return;

def checkIpa():
	if not os.path.exists("%s/%s/%s.ipa"%(Ipa_Path, Scheme, Scheme)):
		print("打包失败");
	else:
		print("包已经打好啦");

def upLoadToFir():
	print("-----------------" + "%s/%s/%s.ipa"%(Ipa_Path, Scheme, Scheme));
	os.system("fir publish %s/%s/%s.ipa -T %s -v"%(Ipa_Path, Scheme, Scheme, FirToken));
	return;

def main():
	#1.设置参数
	setParameters();
	#2.删除旧的编译目录
	deleteOldBuildFile();
	#3.pod更新
	podUpdate();
	#4.创建Archive目录
	createFinder();
	#5.开始编译打包
	buildArchive();
	#6.删除旧的IPA
	importIpa();
	#7.检查是否创建成功
	checkIpa();
	#8.上传Fir
	upLoadToFir();

main();
