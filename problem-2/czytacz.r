filename <- 'signal_50MHz.bin'
zz <- file(filename, "rb")

BajtowNaLiczbe = 4
fsize = file.size(filename)
LiczbaLiczb = fsize / BajtowNaLiczbe
v<-readBin(zz, numeric(), size=BajtowNaLiczbe, endian="little", n=LiczbaLiczb)
close(zz)

print(v[1:10])
plot(v[1:100000], type='l')     # dłuższy fragment
# idx = 67650:67900;
# plot(idx, v[idx],type='l')      # jeden impuls - aby zobaczyć kształt impulsów