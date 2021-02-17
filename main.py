from flask import Flask,jsonify,request,json
from google_trans_new import google_translator
from bs4 import BeautifulSoup
import requests as rq 
from googlesearch import search
import random,wikipedia, time
from covid import Covid
import datetime as dt

kopid=Covid(source="worldometers") 

translet=google_translator()



app=Flask(__name__)
@app.route('/',methods=['POST'])

def main():
	reply=None

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
		
		waktu=str(dt.datetime.now())

		jadi=("tlakir di update : "+waktu+"\n\n"+jadi)

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
		
	if strd[0]==prefix and strd[1]=="time":
		
		reply={"reply":"waktu:\n"+str(dt.datetime.now())}
		
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
		
	if strd[0]==prefix and strd[1]=="doa" and strd[2]=="ulangan":
		
		reply={"reply" :"""Doa Ketika UTBK 2021 akan Dilaksanakan\nاَللَّهُمَّ لاَ سَهْلَ إِلاَّ مَا جَعَلْتَهُ سَهْلاً وَأَنْتَ تَجْعَلُ الْحَزْنَ إِذَا شِئْتَ سَهْلاً\n\nLafadz: Allaahumma laa sahla illaa maa ja’altahu sahlan wa anta taj’alul hazna idzaa syi’ta sahlan.\nArti: Ya Allah! Tidak ada kemudahan kecuali apa yang Engkau jadikan mudah. Sedang yang susah bisa Engkau jadikan mudah, apabila Engkau menghendakinya.\nSumber: Shahih Ibnu Hibban No. 2427 (Syaikh ‘Abdul Qadir Al Arna’uth menyatakan shahih dalam Takhrij Al Adzkar hal. 106)"""} 
		
	if strd[0]==prefix and strd[1]=="doa" and strd[2]=="makan":
		
		reply={"reply":"""Doa Sebelum Makan\n اَللّٰهُمَّ بَارِكْ لَنَا فِيْمَا رَزَقْتَنَا وَقِنَا عَذَابَ النَّارِ \n"Allahumma baarik lanaa fiimaa rozaqtanaa wa qinaa 'adzaa bannaar." \nArtinya: "Ya Allah, berkahilah kami dalam rezeki yang telah Engkau berikan kepada kami dan peliharalah kami dari siksa api neraka."""} 
		
	if strd[0]==prefix and strd[1]=="doa" and strd[2]=="bangun" and strd[3]=="tidur":
		
		reply={"reply" :"Doa bangun tidur lain yang bisa diamalkan muslim dalam versi pendek yang sudah masyhur yakni:\nالْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ \nAlhamdulillahilladzii akhyaana ba'da maa amaatanaa wa ilaihin nusyuur.\nArtinya: Segala puji bagi Allah yang telah menghidupkan kami setelah mematikan kami, dan kepada-Nya lah tempat kembali.\nDoa ini bersumber dari Hadis Nabi SAW dalah sahih Bukhari."} 
		
	if strd[0]==prefix and strd[1]=="doa"and strd[2]=="tidur":
		reply={"reply":"""Doa Sebelum Tidur/foto:istimewa \nبِسْمِكَ اللّهُمَّ اَحْيَا وَ بِسْمِكَ اَمُوْتُ \n“Bismika Allahumma ahyaa wa bismika amuut”.\nArtinya: “Dengan nama-Mu ya Allah aku hidup, dan dengan nama-Mu aku mati”. (HR.Bukhari dan Muslim)."""} 
		
	if strd[0]==prefix and strd[1]=="doa":
		if strd[2]=="belajar":
			
			reply={"reply" :"""Doa sebelum belajar\n\n رَضِتُ بِااللهِ رَبَا وَبِالْاِسْلاَمِ دِيْنَا وَبِمُحَمَّدٍ نَبِيَا وَرَسُوْلاَ رَبِّ زِدْ نِيْ عِلْمًـاوَرْزُقْنِـيْ فَهْمًـا\n\nRodlittu billahiroba, Wabil islaamidiinaa, Wabimuhammadin nabiyyaa warasuula, Robbi zidnii ilmaan warzuqnii fahmaan\n\n “Kami rida Allah SWT sebagai Tuhanku, Islam sebagai agamaku, dan Nabi Muhammad sebagai Nabi dan Rasul, Ya Allah, tambahkanlah kepadaku ilmu dan berikanlah aku pengertian yang baik"."""} 

		if strd[2]=="ayat" and strd[3]=="kursi":
			
			reply ={"reply" :"""Bacaan ayat kursi \nاللهُ لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ مَنْ ذَا الَّذِي يَشْفَعُ عِنْدَهُ إِلَّا بِإِذْنِهِ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ وَلَا يُحِيطُونَ بِشَيْءٍ مِنْ عِلْمِهِ إِلَّا بِمَا شَاءَ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ وَلَا يَئُودُهُ حِفْظُهُمَا وَهُوَ الْعَلِيُّ الْعَظِيمُ\n“Alloohu laa ilaaha illaa huwal hayyul qoyyuum, laa ta’khudzuhuu sinatuw walaa naum. Lahuu maa fissamaawaati wa maa fil ardli man dzal ladzii yasyfa’u ‘indahuu illaa biidznih, ya’lamu maa baina aidiihim wamaa kholfahum wa laa yuhiithuuna bisyai’im min ‘ilmihii illaa bimaa syaa’ wasi’a kursiyyuhus samaawaati wal ardlo walaa ya’uuduhuu hifdhuhumaa wahuwal ‘aliyyul ‘adhiim.” \n\n“Allah, tidak ada Tuhan (yang berhak atau boleh disembah), melainkan Dia yang hidup kekal lagi terus menerus mengurus (makhluk-Nya). Yang tidak mengantuk dan tidak juga tertidur. Kepunyaan-Nya adalah apa yang ada di langit dan apa yang ada di bumi. Tiada yang dapat memberi syafaat di sisi Allah tanpa izin-Nya"."""}

		if strd[2]=="setelah" and strd[3]=="adzan":
			
			reply={"reply":"""Doa Setelah Adzan\nMembaca doa setelah adzan adalah sunnah. Adapun bacaan doa setelah adzan yaitu,\n\n"Allaahumma robba haadzihid da'watit taammah, washsholaatil qoo-imah, aati muhammadanil washiilata wal fadhiilah, wasysyarofa, wad darajatal, 'aaliyatar rofii'ah, wab'atshu maqoomam mahmuudanil ladzii wa'adtah, innaka laa tukhliful mii'aadz."\n\nArtinya:\n"Yaa Allah, Tuhan yang mempunyai seruan yang sempurna dan shalat yang ditegakkan ini, berikanlah dengan limpah karuniaMu kepada Nabi Muhammad kedudukan dan keutamaan (paling tinggi) dan limpahkanlah kepadanya tempat yang terpuji yang telah engkau janjikan"."""}



	if strd[0]==prefix and strd[1]=="sleep" :
		
		
		time.sleep(int(strd[2]))
		
		reply={"reply" :"test"} 
	
	if strd[0]==prefix and strd[1]=="game":
		
		if strd[2]=="jawab":
			
			jawab=int(strd[3])
			
			if data["k"] [0]["tebak"]==jawab:
				reply={"reply":"*GG* lu bener jawabanny adalah" +str(data["k"] [0]["tebak"]) }
			else:
				reply={"reply" :"*BLOK* salah"} 
		if strd [2]=="tebak":
			
			hasilRan=random.randrange(int(strd[3]),int(strd[5]))
			
			jsonFile=open("dataJson.json")
			data=json.load(jsonFile)
			data["k"][0]["tebak"]=hasilRan
		
			aFile=open("dataJson.json","w")
			json.dump(data,aFile)
			aFile.close()
			
			reply={"reply" :"dah coba tebak"} 
			
	if strd[0]==prefix and strd[1]=="ada"and strd[2]=="absen":
		if strd[3]=="ips":
			idPel="1640"
		if strd[3]=="fisika":
			idPel="941"
		if strd[3]=="alq":
			idPel="872"
		if strd[3]=="pkn":
			idPel="938"
		if strd[3]=="bindo":
			idPel="2033"
		if strd[3]=="sbk":
			idPel="1640"
		if strd[3]=="kry":
			idPel="9004"
		if strd[3]=="olga":
			idPel="901"
		if strd[3]=="bing":
			idPel=""
		if strd[3]=="matdas":
			idPel="2896"
		if strd[3]=="agama":
			idPel="2115"
		if strd[3]=="mtk":
			idPel=""
		if strd[3]=="conver":
			idPel=""
			
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
			
	if strd[0]==prefix and strd[1]=="hadits":

		a=rq.get("https://m.bola.com/ragam/read/4268283/25-kata-kata-mutiara-islami-dari-hadist-nabi-menenangkan-dan-memberi-pelajaran") 
		soup=BeautifulSoup(a.text,"html.parser")
		web=soup.findAll("div",{"class":"article-raw-content"})
			
		jadi=web[1].findChildren()

		intny=int(strd[2])

		reply={"reply":jadi[intny]}

	if strd[0]==prefix and strd[1]=="salam" :

		reply={"reply":"""السَّلاَمُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ \nssalamualaikum wa rahmatullahi wa barakatuh.\n\nArtinya  “Salam damai untukmu dan semoga Rahmat serta Keberkahan Allah menyertaimu”. """}
	if strd[0]==prefix and strd[1]=="jawab" and strd[2]=="salam":

		reply={"reply":"""Kemudian bagi yang mendengarnya wajib menjawab dengan ucapan.\n\nوَعَلَيْكُمْ السَّلاَمُ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ\n\nWa ‘alaikum salam wa rahmatullahi wabarakatuh.\n\nArtinya: “Dan semoga keselamatan dan rahmat Allah serta keberhanNya terlimpah juga kepada kalian”"."""}

	if strd[0]==prefix and strd[1]=="ketawa":

		reply={"reply":"aowkkwokwokwo"}

	if strd[0]==prefix and strd[1]=="nofap" and strd[2]=="days":

		   
		ngitunf = dt.date.today()-dt.date(2021,2,17)
		

		reply={"reply":"sudah "+str(ngitunf)+" hari \n\nsejak "+str(dt.date(2021,2,17)) }

	if strd[0]==prefix and strd[1]=="surah":

		nj=strd[-1]

		
		strd.pop(1)
		strd.pop(0)
		strd.pop(-1)

		strj=''.join(strd)
		print(strj)

		a=rq.get("https://litequran.net/"+strj)

		surah=[]

		soup=BeautifulSoup(a.text,"html.parser")

		web=soup.findAll("li")

		for i in range (int(nj)):

			jadi=web[i].findChildren()
			surah.append("ayat"+str(i)+":\n"+jadi[0].text+"\nbacaan :\n"+jadi[1].text+"\narti :\n"+jadi[2].text+"\n\n")

		surahJadi=''.join(surah)
		reply={"reply":surahJadi}

	if strd[0]==prefix and strd[1]=="update":

		reply={"reply":"beta"}
		
	if strd[0]==prefix and strd[1]=="art":

		from pyfiglet import Figlet as fg

		strd.pop(1)
		strd.pop(0)

		jadi=' '.join(strd)

		f=Figlet(font='slant')

		reply={"reply":f.renderText(jadi)}



	if reply==None:

		reply={"g" :"a"} 

	return jsonify(reply)

	
	
	
if __name__ == "__main__":
	main()

