from flask import Flask,jsonify,request,json
from google_trans_new import google_translator
from bs4 import BeautifulSoup
import requests as rq 
from googlesearch import search
import random,wikipedia

 


translet=google_translator()

app=Flask(__name__)
@app.route('/',methods=['POST'])

def main():
	
	sender =request.form["sender"]
	message=request.form["message"]
	
	jsonFile=open("dataJson.json")
	data=json.load(jsonFile)
	
	prefix=data["k"][0]["prefix"]
	
	strd = message.split(" ")
	
	if strd[0]==prefix and strd[1]=="tugas":
		reply={"reply":"*TUGAS NYA ADALAH*\n"+ data["k"][0]["tugas"]}
		
	if strd[0]==prefix and strd[1]=="note":
		reply={"reply":data["k"] [1]["note"]}
		
	if strd[0]==prefix and strd[1]=="ubahtugas":
		
		strd.pop(1)
		strd.pop(0)
		
		jadi =' '.join(strd)
		
		jsonFile=open("dataJson.json")
		data=json.load(jsonFile)
		data["k"][0]["tugas"]=jadi
		
		aFile=open("dataJson.json","w")
		json.dump(data,aFile)
		aFile.close()
		
		reply={"reply":"*TUGAS DIUBAH MENJADI*\n"+ data["k"][0]["tugas"]}
		
	if strd[0]==prefix and strd[1]=="ubahnote":
		
		strd.pop(1)
		strd.pop(0)
		
		jadi =' '.join(strd)
		
		jsonFile=open("dataJson.json")
		data=json.load(jsonFile)
		data["k"][1]["note"]=jadi
		
		aFile=open("dataJson.json","w")
		json.dump(data,aFile)
		aFile.close()
		
		reply={"reply":"tugas berhasil diubah✅" }
		
	if strd[0]==prefix and strd[1]  =="ubahprefix":
		

		
		jadi =strd[2]
		
		jsonFile=open("dataJson.json")
		data=json.load(jsonFile)
		data["k"][0]["prefix"]=jadi
		
		aFile=open("dataJson.json","w")
		json.dump(data,aFile)
		aFile.close()
		
		reply={"reply":"*PREFIX DIUBAH MENJADI*\n"+ data["k"][0]["prefix"]}
		return jsonify(reply)
	
	if strd[0]==prefix and strd[1]=="ngomong":
		
		strd.pop(1)
		strd.pop(0)
		
		jadi=' '.join(strd)
		
		reply={"reply":"*BOT*\n"+jadi}
		
	if message =="prefix":
		
		reply={"reply":"*PREFIXNYA ITU*"+data["k"][0]["prefix"]}
		return jsonify(reply)
		
	if strd[0]==prefix and strd[1]=="translet":
		
		strd.pop(1)
		strd.pop(0)

		jadi =' '.join(strd)
		
		if strd[-1]=="id":
	
			jadi=translet.translate(jadi,lang_tgt='id')
		else:
			jadi= translet.translate(jadi,lang_tgt=strd[-1])
		
		reply={"reply":"trasnlet jadi\n"+jadi}
		
	if strd[0]==prefix and strd[1]=="covid":
		if strd[2]=="indo":
			
	    
			page =rq.get('https://covid19.go.id')
	     
			soup=BeautifulSoup(page.text,'html.parser')
	    
			div=soup.findAll('div',{'class':'col-md-3 text-color-black p-4'})
	    
			reply={"reply":div[1].text}
		
		if strd[2]=="bontang":
			
			a =rq.get("http://gugus-covid.bontangkota.go.id/?page_id=556")
			soup=BeautifulSoup(a.text,'html.parser')
			div=soup.findAll('div',{'data-number-value':True})
		
			jadi="yang positip :" +div[0].get("data-number-value")+"\nyang sembuh:"+div[1].get("data-number-value")+"\nyang meninggoy:" +div[2].get("data-number-value")+"\nsource: http://gugus-covid.bontangkota.go.id/?page_id=556" 

			reply={"reply":jadi}
			
	    
	    if strd[2]=="total":
			if strd[3]=="aktif":
				
				aktip=kopid.get_total_active_cases()
			
				reply={"reply":str(aktip)+" total yg aktip 1dunia"}

			if strd[3]=="mati":
				
				mati=kopid.get_total_deaths()
				
				reply={"reply":str(mati)+" total yang Innalilahi"}
			
			if strd[3]=="sembuh":
				
				smbuh=kopid.get_total_recovered()
				
				reply={"reply":str(smbuh)+" total yang Alhamdulillah"}
			
			if strd[3]=="konfirm":
				
				konfirm=kopid.get_total_confirmed_cases()
				
				reply={"reply":str(konfirm)+" yang ke konfirm"}
			else:
				try:
					n=kopid.get_status_by_country_name(strd[2])
					reply={"reply":str(n['country'])+"\n"+str(n['confirmed'])+"confirmed\n"+str(n['active'])+"yang aktip\n"+str(n['deaths'])+" yang meninggal\n"+str(n['recovered'])+" yang sembuh"}
					
				except:
					reply={"reply":"negara apa itu goblok! gaad"}
	    
	
	if strd[0]==prefix and strd[1]=="cari":
        
		strd.pop(1)
		strd.pop(0)
        
		a=[]

		jadi =' '.join(strd)
        
        
		for j in search(jadi, tld="co.in", num=10, stop=10, pause=1): 
			a.append(j)

		hasilS='\n\n'.join(a)
		reply={"reply":"hasi pencarian untuk"+jadi+"adalah\n\n" + hasilS}
		
	if strd[0]==prefix and strd[1]=="randomdari" :
		 
		 
		hasilRan=random.randrange(int(strd[2]) ,int(strd[4]))
		reply={"reply" :hasilRan} 
		
	if strd[0]==prefix and strd[1]=="apakah" and strd[-1]=="cocok":
		 
		hasilRand=str(random.randrange(1,100)) 
		
		reply={"reply" :strd[2] +" dan " +strd[4] +"  *" +hasilRand +"%*"+" cocok" }
 

 
	if strd[0]==prefix and strd[1]=="apaka" :
		
		a=strd[-1]
		
		strd.pop(-1)
		strd.pop(1)
		strd.pop(0)
		
		jadi =" ".join(strd)
		
		hasilRan=random.randrange(1,100) 
		reply={"reply":"hasil:\n*kata ilham* "+jadi+" *"+str(hasilRan) +"%* "+a }
		
	if strd[0]==prefix and strd[1]=="wiki" :
		
		strd.pop(1)
		strd.pop(0)
		
		jadi=' '.join(strd)
		
		wikipedia.set_lang("id") 
		hasilW=wikipedia.summary(jadi)
		
		reply={"reply":hasilW}
		
	if strd[0]==prefix and strd[1]=="wiki" and strd[2]=="cari":
		
		hasilW=wikipedia.search(strd[3])
		hasilW=" ".join(hasilW)
		
		reply={"reply":"hasil:\n"+hasilW}
		
	if strd[0]==prefix and strd[1]=="random"and strd[2]=="hadits":
		
		a=rq.get("https://m.bola.com/ragam/read/4268283/25-kata-kata-mutiara-islami-dari-hadist-nabi-menenangkan-dan-memberi-pelajaran") 
		soup=BeautifulSoup(a.text,"html.parser")
		web=soup.findAll("div",{"class":"article-raw-content"})
		
		jadi=web[1].findChildren()
		
		listHadist=[jadi[0].text,jadi[1].text,jadi[2].text,jadi[3].text,jadi[4].text,jadi[5].text,jadi[6].text,jadi[7].text,jadi[8].text,jadi[9].text]
		rndom=random.choice(listHadist)
		
		print (rndom) 
		
		reply={"reply":rndom}
		
	if strd[0]==prefix and strd[1]=="pilih" :
		
		strd.pop(1)
		strd.pop(0)
		
		listny=strd[0:9999]
		
		hasilRndom=random.choice(listny)
		
		reply={"reply":"*kata ilham* mending "+ hasilRndom}
		
	if strd[0]==prefix and strd[1]=="doa" and strd[2]=="makan":
		
		reply={"reply":"""Doa Sebelum Makan\n اَللّٰهُمَّ بَارِكْ لَنَا فِيْمَا رَزَقْتَنَا وَقِنَا عَذَابَ النَّارِ \n"Allahumma baarik lanaa fiimaa rozaqtanaa wa qinaa 'adzaa bannaar." \nArtinya: "Ya Allah, berkahilah kami dalam rezeki yang telah Engkau berikan kepada kami dan peliharalah kami dari siksa api neraka."""} 
		
	if strd[0]==prefix and strd[1]=="doa"and strd[2]=="tidur":
		reply={"reply":"""Doa Sebelum Tidur/foto:istimewa \nبِسْمِكَ اللّهُمَّ اَحْيَا وَ بِسْمِكَ اَمُوْتُ \n“Bismika Allahumma ahyaa wa bismika amuut”.\nArtinya: “Dengan nama-Mu ya Allah aku hidup, dan dengan nama-Mu aku mati”. (HR.Bukhari dan Muslim)."""} 
		
	if strd[0]==prefix and strd[1]=="doa":
		if strd[2]=="belajar":
			reply={"reply" :"""Doa sebelum belajar\n\n رَضِتُ بِااللهِ رَبَا وَبِالْاِسْلاَمِ دِيْنَا وَبِمُحَمَّدٍ نَبِيَا وَرَسُوْلاَ رَبِّ زِدْ نِيْ عِلْمًـاوَرْزُقْنِـيْ فَهْمًـا\n\nRodlittu billahiroba, Wabil islaamidiinaa, Wabimuhammadin nabiyyaa warasuula, Robbi zidnii ilmaan warzuqnii fahmaan\n\n “Kami rida Allah SWT sebagai Tuhanku, Islam sebagai agamaku, dan Nabi Muhammad sebagai Nabi dan Rasul, Ya Allah, tambahkanlah kepadaku ilmu dan berikanlah aku pengertian yang baik"."""} 
		if strd[2]=="ayat" and strd[3]=="kursi":
			
			reply ={"reply" :"""Bacaan ayat kursi \nاللهُ لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ مَنْ ذَا الَّذِي يَشْفَعُ عِنْدَهُ إِلَّا بِإِذْنِهِ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ وَلَا يُحِيطُونَ بِشَيْءٍ مِنْ عِلْمِهِ إِلَّا بِمَا شَاءَ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ وَلَا يَئُودُهُ حِفْظُهُمَا وَهُوَ الْعَلِيُّ الْعَظِيمُ\n“Alloohu laa ilaaha illaa huwal hayyul qoyyuum, laa ta’khudzuhuu sinatuw walaa naum. Lahuu maa fissamaawaati wa maa fil ardli man dzal ladzii yasyfa’u ‘indahuu illaa biidznih, ya’lamu maa baina aidiihim wamaa kholfahum wa laa yuhiithuuna bisyai’im min ‘ilmihii illaa bimaa syaa’ wasi’a kursiyyuhus samaawaati wal ardlo walaa ya’uuduhuu hifdhuhumaa wahuwal ‘aliyyul ‘adhiim.” \n\n“Allah, tidak ada Tuhan (yang berhak atau boleh disembah), melainkan Dia yang hidup kekal lagi terus menerus mengurus (makhluk-Nya). Yang tidak mengantuk dan tidak juga tertidur. Kepunyaan-Nya adalah apa yang ada di langit dan apa yang ada di bumi. Tiada yang dapat memberi syafaat di sisi Allah tanpa izin-Nya"."""}

	if strd[0]==prefix and strd[1]=="ada"and strd[2]=="absen":
		if strd[3]=="ips":
			idPel="1640"
		if strd[3]=="fisika":
			idPel="941"
		if strd[3]=="alq":
			idPel="872"
		if strd[3]=="pkn":
			idPel="938"
		if strd[3]="bindo":
			idPel="2033"
			
		s=rq.session()

		a=s.get("https://elearning.smpypvdp.sch.id/login/index.php") 

		soup=BeautifulSoup(a.text,"html.parser")

		a=soup.find("input",{"name":"logintoken"})

		b=a.get("value")
			



		login={"username":"6531","password":"2252006","logintoken":b,"anchor":""}

		ewq=s.post("https://elearning.smpypvdp.sch.id/login/index.php",login)

		


		jh =BeautifulSoup(s.get("https://elearning.smpypvdp.sch.id/mod/attendance/view.php?id=" +idPel+"&view=1").text,"html.parser")

		bod=jh.findAll("tr",{"class":"lastrow"})

		if bod: 
			reply={"reply" :b+"\n\n"+str(ewq.status_code) +"\n\nAda Absen\n"+bod[1].text}
		else:
			reply={"reply" :b+"\n\n"+str(ewq.status_code) +"\n\n"+bod[1].text}
			
		
		

	return jsonify(reply)

	
	
	
if __name__ == "__main__":
	main()

