filename <- 'signal_50MHz.bin'
zz <- file(filename, "rb")

BajtowNaLiczbe = 4
fsize = file.size(filename)
LiczbaLiczb = fsize / BajtowNaLiczbe
v<-readBin(zz, numeric(), size=BajtowNaLiczbe, endian="little", n=LiczbaLiczb)
close(zz)

print(v[1:10])
png("problem-2/wykresy/dluzszy_fragment_sygnalu.png")
plot(v[1:100000], type='l', main='Dluzszy fragment sygnalu', xlab='Przedzial', ylab='Wartosc natezenia') # dluzszy fragment sygnalu
dev.off()

png("problem-2/wykresy/pojedynczy_impuls.png")
idx = 67650:67900;
plot(idx, v[idx],type='l', main='Pojedynczy impuls', xlab='Przedzial', ylab='Wartosc natezenia')      # jeden impuls - aby zobaczyć kształt impulsów
dev.off()

# Zadanie 2

# Ustawienie progu detekcji impulsów na 95% kwantyla
threshold = quantile(v, 0.95)

print(threshold)

# Znajdź indeksy, gdzie sygnał przekracza próg (indeksy impulsów)
impulse_indices <- which(v > threshold)

# Znajdź indeksy, gdzie sygnał nie przekracza progu (indeksy nie-impulsów)
non_impulse_indices <- setdiff(1:length(v), impulse_indices)

#a)
# Analiza fragmentu sygnału bez impulsów
non_impulse_signal <- v[non_impulse_indices]

# Wykres histogramu
png("problem-2/wykresy/histogram_szumu.png")
hist(non_impulse_signal, main="Histogram sygnału bez impulsow", xlab="Natezenie sygnalu", ylab="Liczebnosc", col="lightblue")
dev.off()

#b)Badanie rozkładu odstępów czasu między impulsami

# Znajdź odstępy czasu między impulsami
time_gaps <- diff(impulse_indices)

# Zatrzymaj wieksze od 100, czyli roznica miedzy koncem jednego a poczatkiem drugiego impulsu
time_gaps_filtered <- time_gaps[time_gaps > 100]

# Przelicz odstępy czasu na ilość próbek
ilosc_probek_miedzy_impulsami <- time_gaps_filtered / 50e6  # Przeliczamy na ilość próbek, gdzie 50e6 to częstotliwość próbkowania 50 MHz

png("problem-2/wykresy/histogram_odstepu_czasu.png")
hist(ilosc_probek_miedzy_impulsami, main = "Histogram odstępów czasu miedzy impulsami", xlab = "Odstep czasu", ylab = "Liczebnosc", col = "lightgreen")
dev.off()
