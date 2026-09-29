/* read words (one per line) on stdin; print eSpeak NG en-us IPA phonemes, '_'-separated, one line per word */
#include <stdio.h>
#include <string.h>
#include <espeak-ng/speak_lib.h>
int main(int argc,char**argv){
  if(espeak_Initialize(AUDIO_OUTPUT_RETRIEVAL,0,argv[1],0)<0){ fprintf(stderr,"init failed\n"); return 1; }
  if(espeak_SetVoiceByName(argc>2?argv[2]:"en-us")!=EE_OK){ fprintf(stderr,"voice failed\n"); return 1; }
  char line[512];
  while(fgets(line,sizeof line,stdin)){
    line[strcspn(line,"\r\n")]=0;
    const void *p=line; char out[4096]; out[0]=0;
    while(p){ const char *ph=espeak_TextToPhonemes(&p,espeakCHARS_UTF8,0x02|('_'<<8));
      if(ph){ if(out[0]) strncat(out," ",sizeof out-strlen(out)-1); strncat(out,ph,sizeof out-strlen(out)-1); } }
    printf("%s\n",out); fflush(stdout);
  }
  return 0;
}
