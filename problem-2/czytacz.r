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

# Ustawienie progu detekcji impulsów na 0.01 jednostki nateżenia
threshold = quantile(v, 0.9997)
print(threshold)

# Znajdź indeksy, gdzie sygnał przekracza próg (indeksy impulsów)
impulse_indices <- which(v > threshold)
# Oblicz autokorelację sygnału
autocorr <- acf(v, plot=FALSE)
# Wykreśl funkcję autokorelacji
png("problem-2/wykresy/autokorelacja.png")
plot(autocorr, main="Autokorelacja sygnalu")
dev.off()


# Wykres części sygnału z zaznaczonymi impulsami
idx_max = length(v)/20
v_part = v[0 : idx_max]
impulse_indices_part = impulse_indices[impulse_indices <= idx_max]
png("problem-2/wykresy/jeden-fragment_zaznaczone-impulsy.png")
plot(v_part, type = 'l', main = "Sygnał z wykrytymi impulsami", xlab="Indeks", ylab="Natężenie")
points(impulse_indices_part, v[impulse_indices_part], col = 'blue', pch = 16)
dev.off()


idx = 67650:67900;
png("problem-2/wykresy/fragment_zaznaczone-impulsy.png")
plot(idx, v[idx],type='l', xlab="Indeks", ylab="Natężenie")# jeden impuls - aby zobaczyć kształt impulsów
impulse_indices2 = impulse_indices[impulse_indices >= 67650]
impulse_indices2 = impulse_indices2[impulse_indices2 <= 67900]
points(impulse_indices2, v[impulse_indices2], col = 'blue', pch = 16)
dev.off()


# Znajdź indeksy, gdzie sygnał nie przekracza progu (indeksy nie-impulsów)
non_impulse_indices <- setdiff(1:length(v), impulse_indices)

#a)
# Analiza fragmentu sygnału bez impulsów
non_impulse_signal <- v[non_impulse_indices]

# Oblicz średnią i odchylenie standardowe sygnału
mean_signal <- mean(non_impulse_signal)
print("Srednia sygnalu")
print(mean_signal)
sd_signal <- sd(non_impulse_signal)
print("Odchylenie standardowe sygnalu")
print(sd_signal)

# Generuj sekwencję liczb dla osi x
x <- seq(min(non_impulse_signal), max(non_impulse_signal), length.out = 100)

# Oblicz wartości funkcji Gaussa dla wygenerowanych liczb
y <- dnorm(x, mean=mean_signal, sd=sd_signal)

# Dodaj dopasowaną funkcję Gaussa do histogramu
png("problem-2/wykresy/histogram_szumu_gauss.png")
hist(non_impulse_signal, main="Histogram sygnału bez impulsow z dopasowaniem Gaussa", xlab="Natezenie sygnalu", ylab="Liczebnosc", col="lightblue", freq=FALSE)
lines(x, y, col="red")
dev.off()


png("problem-2/wykresy/wykres-pudelkowy-szumu.png")
boxplot(non_impulse_signal, main="Wykres pudełkowy Sygnału bez Impulsów", xlab="Natężenie", ylab="Liczebność", col="lightblue")
dev.off()

#b)Badanie rozkładu odstępów czasu między impulsami

# Znajdź odstępy czasu między impulsami
ilosc_probek_miedzy_impulsami <- diff(impulse_indices)

# Wybierz tylko te odstępy czasu, które są wystarczająco długie
time_gaps <- ilosc_probek_miedzy_impulsami[ilosc_probek_miedzy_impulsami > 200]

# Przelicz odstępy czasu na ilość próbek
time_gaps = time_gaps / 50e6 * 1000  # Przeliczamy na ilość próbek, gdzie 50e6 to częstotliwość próbkowania 50 MHz, a 1000 to przelicznik na milisekundy

num_breaks <- 30
png("problem-2/wykresy/histogram_odstepu_czasu.png")
hist(time_gaps, breaks = num_breaks, main = "Histogram odstępów czasu miedzy impulsami", xlab = "Odstep czasu w ms", ylab = "Liczebnosc", col = "lightgreen")
dev.off()

# Podziel impulsy na grupy
chunks <- split(v, ceiling(seq_along(v)/200))
# Znajdź maksymalną wartość w każdej grupie
max_values <- sapply(chunks, max)
# Odfiltruj wartości, które są wieksze od 0.01 i mniejsze od 1
filtered_max_values <- max_values[max_values >= 0.005 & max_values <= 1]

# Wykreśl histogram maksymalnych impulsów
png("problem-2/wykresy/max_impulsy_histogram.png")
hist(filtered_max_values, main = "Histogram of Max Impulses", xlab = "Amplitude", ylab = "Frequency", col = "lightblue")
dev.off()