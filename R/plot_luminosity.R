get_col_vec <- function(x1, x2, thr1, thr2) {
ttl_lilac <- rgb(160/255, 40/255, 140/255)

    cv <-  rep("white", length(x1))
    ind <- (x1 >= thr1) & (x2 >= thr2)
    cv[ind] <- ttl_lilac
    cv
}

read_data <- function(f) {
    df <- read.csv(f, sep = "\t", header = FALSE, col.names = c("hour", "minute", "value"))
    df$time <- paste0(df$hour, ":", df$minute)
    df$time <- as.POSIXct(df$time, format = "%H:%M")
    df
}

data <- read_data("../data/iot_log.csv")

## define colours
ttl_blue <- rgb(0/255, 60/255, 120/255)
ttl_lilac <- rgb(160/255, 40/255, 140/255)

t0 <- as.POSIXct("08:27", format = "%H:%M")

t1 <- as.POSIXct("11:00", format = "%H:%M")
t2 <- as.POSIXct("12:05", format = "%H:%M")

t3 <- as.POSIXct("13:03", format = "%H:%M")
t4 <- as.POSIXct("14:06", format = "%H:%M")

## pdf("../figures/Fig9.pdf", width = 5.2, height = 2.5, pointsize = 3)
postscript("../../figures/ready/Fig9.eps", width = 5.2, height = 2.5, pointsize = 3, horizontal = FALSE, onefile = FALSE, paper = "special")
plot(data$time, data$value, type = "l", col = ttl_blue, xlab = "Time", ylab = "Luminosity [arbitrary units]", lwd = 2.5, ylim = c(850, 1000))
abline(v = t0, col = ttl_lilac, lwd = 2, lty = 2)
abline(v = t1, col = ttl_lilac, lwd = 2, lty = 2)
abline(v = t2, col = ttl_lilac, lwd = 2, lty = 2)
abline(v = t3, col = ttl_lilac, lwd = 2, lty = 2)
abline(v = t4, col = ttl_lilac, lwd = 2, lty = 2)

text(x = t0, y = 990, pos = 4, "arrived at work\nnot turning on lights", col = ttl_lilac)
text(x = t1, y = 990, pos = 4, "lights on", col = ttl_lilac)
text(x = t2, y = 990, pos = 4, "out for lunch\nlights off", col = ttl_lilac)
text(x = t3, y = 990, pos = 4, "back in office\nlights on", col = ttl_lilac)
text(x = t4, y = 990, pos = 4, "lights off", col = ttl_lilac)
dev.off()



