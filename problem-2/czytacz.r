filename <- 'signal_50MHz.bin'
zz <- file(filename, "rb")

BajtowNaLiczbe = 4
fsize = file.size(filename)
LiczbaLiczb = fsize / BajtowNaLiczbe
v<-readBin(zz, numeric(), size=BajtowNaLiczbe, endian="little", n=LiczbaLiczb)
close(zz)

print(v[1:10])
plot(v[1:100000], type='l')     # dłuższy fragment
idx = 67650:67900;
plot(idx, v[idx],type='l')      # jeden impuls - aby zobaczyć kształt impulsów

# Zadanie 2

# Ustawienie progu detekcji impulsów na 90% kwantyla
threshold = quantile(v, 0.90)

print(threshold)

# Znajdź indeksy, gdzie sygnał przekracza próg (indeksy impulsów)
impulse_indices <- which(v > threshold)

# Znajdź indeksy, gdzie sygnał nie przekracza progu (indeksy nie-impulsów)
non_impulse_indices <- setdiff(1:length(v), impulse_indices)

# Wykres sygnału z zaznaczonymi impulsami
plot(v, type = 'l', main = "Sygnał z wykrytymi impulsami")
points(non_impulse_indices, v[non_impulse_indices], col = 'blue', pch = 16)


#a)
# Analiza fragmentu sygnału bez impulsów
non_impulse_signal <- v[non_impulse_indices]

# Wykres histogramu
hist(non_impulse_signal, main="Histogram Sygnału bez Impulsów", xlab="Wartość", ylab="Liczebność", col="lightblue")

#b)Badanie rozkładu odstępów czasu między impulsami

# Znajdź odstępy czasu między impulsami
time_gaps <- diff(impulse_indices)

# Przelicz odstępy czasu na ilość próbek
ilosc_probek_miedzy_impulsami <- time_gaps * 50e6  # Przeliczamy na ilość próbek, gdzie 50e6 to częstotliwość próbkowania 50 MHz
print(ilosc_probek_miedzy_impulsami)

# Wybierz tylko te odstępy czasu, które są wystarczająco krótkie
short_time_gaps <- ilosc_probek_miedzy_impulsami[ilosc_probek_miedzy_impulsami < 1000000]
print(short_time_gaps)


# Sprawdź, czy short_time_gaps nie jest puste
if (length(short_time_gaps) > 0) {
  num_breaks <- 30

  # Wykres histogramu odstępów czasu
  hist(short_time_gaps, breaks = num_breaks, main = "Histogram Krótkich Odstępów Czasu Między Impulsami", xlab = "Odstęp czasu", ylab = "Liczebność", col = "lightgreen")
} else {
  cat("Brak danych do wygenerowania histogramu.\n")
}

