import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import UNIT_VOLT, UNIT_PERCENT, ICON_FLASH, ICON_GAUGE

DEPENDENCIES = ["uart"]

qpigs_parser_ns = cg.esphome_ns.namespace("qpigs_parser")
QPIGSParser = qpigs_parser_ns.class_("QPIGSParser", cg.Component)

CONF_UART_ID = "uart_id"
CONF_AC_INPUT_VOLTAGE = "ac_input_voltage"
CONF_AC_OUTPUT_VOLTAGE = "ac_output_voltage"
CONF_LOAD_PERCENT = "load_percent"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(QPIGSParser),
    cv.Required(CONF_UART_ID): cv.use_id(uart.UARTComponent),
    cv.Required(CONF_AC_INPUT_VOLTAGE): sensor.sensor_schema(unit_of_measurement=UNIT_VOLT, icon=ICON_FLASH),
    cv.Required(CONF_AC_OUTPUT_VOLTAGE): sensor.sensor_schema(unit_of_measurement=UNIT_VOLT, icon=ICON_FLASH),
    cv.Required(CONF_LOAD_PERCENT): sensor.sensor_schema(unit_of_measurement=UNIT_PERCENT, icon=ICON_GAUGE),
})

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_UART_ID])
    await cg.register_component(var, config)
    uart_comp = await cg.get_variable(config[CONF_UART_ID])
    cg.add(var.set_uart(uart_comp))

    sens1 = await sensor.new_sensor(config[CONF_AC_INPUT_VOLTAGE])
    cg.add(var.set_input_voltage_sensor(sens1))

    sens2 = await sensor.new_sensor(config[CONF_AC_OUTPUT_VOLTAGE])
    cg.add(var.set_output_voltage_sensor(sens2))

    sens3 = await sensor.new_sensor(config[CONF_LOAD_PERCENT])
    cg.add(var.set_load_sensor(sens3))
