#include "bmp280.h"
#include "main.h"
#include "i2c.h"
#include <stdio.h>

extern I2C_HandleTypeDef hi2c1;

uint8_t BMP280_ReadID(void)
{
    uint8_t tx_data = BMP280_REG_ID;
    uint8_t rx_data = 0;
    HAL_StatusTypeDef status;

    status = HAL_I2C_Master_Transmit(&hi2c1, BMP280_I2C_ADDR, &tx_data, 1, HAL_MAX_DELAY);
    if (status != HAL_OK)
    {
        printf("BMP280_ReadID: Error transmitting register address (0x%02X)\r\n", tx_data);
        return 0;
    }

    // Receive ID
    status = HAL_I2C_Master_Receive(&hi2c1, BMP280_I2C_ADDR, &rx_data, 1, HAL_MAX_DELAY);
    if (status != HAL_OK)
    {
        printf("BMP280_ReadID: Error receiving data\r\n");
        return 0;
    }

    return rx_data;
}

void BMP280_Init(void)
{
    uint8_t chip_id = BMP280_ReadID();
    if (chip_id == BMP280_CHIP_ID)
    {
        printf("BMP280 detected with ID: 0x%02X\r\n", chip_id);
    }
    else
    {
        printf("BMP280 not detected. Expected ID: 0x%02X, Got: 0x%02X\r\n", BMP280_CHIP_ID, chip_id);
    }
}
