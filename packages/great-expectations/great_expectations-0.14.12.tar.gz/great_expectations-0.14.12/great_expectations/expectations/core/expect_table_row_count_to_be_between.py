from typing import Dict, Optional

from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.execution_engine import ExecutionEngine
from great_expectations.expectations.expectation import TableExpectation
from great_expectations.expectations.util import render_evaluation_parameter_string
from great_expectations.render.renderer.renderer import renderer
from great_expectations.render.types import RenderedStringTemplateContent
from great_expectations.render.util import (
    handle_strict_min_max,
    parse_row_condition_string_pandas_engine,
    substitute_none_for_missing,
)
from great_expectations.rule_based_profiler.config import RuleBasedProfilerConfig


class ExpectTableRowCountToBeBetween(TableExpectation):
    """Expect the number of rows to be between two values.

    expect_table_row_count_to_be_between is a :func:`expectation \
    <great_expectations.validator.validator.Validator.expectation>`, not a
    ``column_map_expectation`` or ``column_aggregate_expectation``.

    Keyword Args:
        min_value (int or None): \
            The minimum number of rows, inclusive.
        max_value (int or None): \
            The maximum number of rows, inclusive.

    Other Parameters:
        result_format (str or None): \
            Which output mode to use: `BOOLEAN_ONLY`, `BASIC`, `COMPLETE`, or `SUMMARY`.
            For more detail, see :ref:`result_format <result_format>`.
        include_config (boolean): \
            If True, then include the expectation config as part of the result object. \
            For more detail, see :ref:`include_config`.
        catch_exceptions (boolean or None): \
            If True, then catch exceptions and include them as part of the result object. \
            For more detail, see :ref:`catch_exceptions`.
        meta (dict or None): \
            A JSON-serializable dictionary (nesting allowed) that will be included in the output without \
            modification. For more detail, see :ref:`meta`.

    Returns:
        An ExpectationSuiteValidationResult

        Exact fields vary depending on the values passed to :ref:`result_format <result_format>` and
        :ref:`include_config`, :ref:`catch_exceptions`, and :ref:`meta`.

    Notes:
        * min_value and max_value are both inclusive.
        * If min_value is None, then max_value is treated as an upper bound, and the number of acceptable rows has \
          no minimum.
        * If max_value is None, then min_value is treated as a lower bound, and the number of acceptable rows has \
          no maximum.

    See Also:
        expect_table_row_count_to_equal
    """

    library_metadata = {
        "maturity": "production",
        "tags": ["core expectation", "table expectation"],
        "contributors": [
            "@great_expectations",
        ],
        "requirements": [],
        "has_full_test_suite": True,
        "manually_reviewed_code": True,
    }

    metric_dependencies = ("table.row_count",)
    success_keys = (
        "min_value",
        "max_value",
        "auto",
        "profiler_config",
    )

    default_profiler_config: RuleBasedProfilerConfig = RuleBasedProfilerConfig(
        name="expect_table_row_count_to_be_between",  # Convention: use "expectation_type" as profiler name.
        config_version=1.0,
        class_name="RuleBasedProfilerConfig",
        module_name="great_expectations.rule_based_profiler",
        variables={
            "false_positive_rate": 0.05,
            "estimator": "bootstrap",
            "num_bootstrap_samples": 9999,
            "bootstrap_random_seed": None,
            "round_decimals": 0,
            "truncate_values": {
                "lower_bound": 0,
                "upper_bound": None,
            },
        },
        rules={
            "default_expect_table_row_count_to_be_between_rule": {
                "domain_builder": {
                    "class_name": "TableDomainBuilder",
                    "module_name": "great_expectations.rule_based_profiler.domain_builder",
                },
                "parameter_builders": [
                    {
                        "name": "row_count_range",
                        "class_name": "NumericMetricRangeMultiBatchParameterBuilder",
                        "module_name": "great_expectations.rule_based_profiler.parameter_builder",
                        "metric_name": "table.row_count",
                        "metric_domain_kwargs": None,
                        "metric_value_kwargs": None,
                        "enforce_numeric_metric": True,
                        "replace_nan_with_zero": True,
                        "reduce_scalar_metric": True,
                        "false_positive_rate": "$variables.false_positive_rate",
                        "estimator": "$variables.estimator",
                        "num_bootstrap_samples": "$variables.num_bootstrap_samples",
                        "bootstrap_random_seed": "$variables.bootstrap_random_seed",
                        "round_decimals": "$variables.round_decimals",
                        "truncate_values": "$variables.truncate_values",
                        "json_serialize": True,
                    },
                ],
                "expectation_configuration_builders": [
                    {
                        "expectation_type": "expect_table_row_count_to_be_between",
                        "class_name": "DefaultExpectationConfigurationBuilder",
                        "module_name": "great_expectations.rule_based_profiler.expectation_configuration_builder",
                        "min_value": "$parameter.row_count_range.value.value_range[0]",
                        "max_value": "$parameter.row_count_range.value.value_range[1]",
                        "meta": {
                            "profiler_details": "$parameter.row_count_range.details",
                        },
                    }
                ],
            },
        },
    )

    default_kwarg_values = {
        "min_value": None,
        "max_value": None,
        "result_format": "BASIC",
        "include_config": True,
        "catch_exceptions": False,
        "meta": None,
        "auto": False,
        "profiler_config": default_profiler_config,
    }
    args_keys = (
        "min_value",
        "max_value",
    )

    def validate_configuration(
        self, configuration: Optional[ExpectationConfiguration]
    ) -> bool:
        """
        Validates that a configuration has been set, and sets a configuration if it has yet to be set. Ensures that
        necessary configuration arguments have been provided for the validation of the expectation.

        Args:
            configuration (OPTIONAL[ExpectationConfiguration]): \
                An optional Expectation Configuration entry that will be used to configure the expectation
        Returns:
            True if the configuration has been validated successfully. Otherwise, raises an exception
        """

        # Setting up a configuration
        super().validate_configuration(configuration)
        self.validate_metric_value_between_configuration(configuration=configuration)

        return True

    @classmethod
    def _atomic_prescriptive_template(
        cls,
        configuration=None,
        result=None,
        language=None,
        runtime_configuration=None,
        **kwargs,
    ):
        runtime_configuration = runtime_configuration or {}
        include_column_name = runtime_configuration.get("include_column_name", True)
        include_column_name = (
            include_column_name if include_column_name is not None else True
        )
        styling = runtime_configuration.get("styling")
        params = substitute_none_for_missing(
            configuration.kwargs,
            [
                "min_value",
                "max_value",
                "row_condition",
                "condition_parser",
                "strict_min",
                "strict_max",
            ],
        )
        # format params
        params_with_json_schema = {
            "min_value": {
                "schema": {"type": "number"},
                "value": params.get("min_value"),
            },
            "max_value": {
                "schema": {"type": "number"},
                "value": params.get("max_value"),
            },
            "condition_parser": {
                "schema": {"type": "string"},
                "value": params.get("condition_parser"),
            },
            "strict_min": {
                "schema": {"type": "boolean"},
                "value": params.get("strict_min"),
            },
            "strict_max": {
                "schema": {"type": "boolean"},
                "value": params.get("strict_max"),
            },
        }

        if params["min_value"] is None and params["max_value"] is None:
            template_str = "May have any number of rows."
        else:
            at_least_str, at_most_str = handle_strict_min_max(params)

            if params["min_value"] is not None and params["max_value"] is not None:
                template_str = f"Must have {at_least_str} $min_value and {at_most_str} $max_value rows."
            elif params["min_value"] is None:
                template_str = f"Must have {at_most_str} $max_value rows."
            elif params["max_value"] is None:
                template_str = f"Must have {at_least_str} $min_value rows."

        if params["row_condition"] is not None:
            (
                conditional_template_str,
                conditional_params,
            ) = parse_row_condition_string_pandas_engine(
                params["row_condition"], with_schema=True
            )
            template_str = (
                conditional_template_str
                + ", then "
                + template_str[0].lower()
                + template_str[1:]
            )
            params_with_json_schema.update(conditional_params)

        return (template_str, params_with_json_schema, styling)

    @classmethod
    @renderer(renderer_type="renderer.prescriptive")
    @render_evaluation_parameter_string
    def _prescriptive_renderer(
        cls,
        configuration=None,
        result=None,
        language=None,
        runtime_configuration=None,
        **kwargs,
    ):
        runtime_configuration = runtime_configuration or {}
        include_column_name = runtime_configuration.get("include_column_name", True)
        include_column_name = (
            include_column_name if include_column_name is not None else True
        )
        styling = runtime_configuration.get("styling")
        params = substitute_none_for_missing(
            configuration.kwargs,
            [
                "min_value",
                "max_value",
                "row_condition",
                "condition_parser",
                "strict_min",
                "strict_max",
            ],
        )

        if params["min_value"] is None and params["max_value"] is None:
            template_str = "May have any number of rows."
        else:
            at_least_str, at_most_str = handle_strict_min_max(params)

            if params["min_value"] is not None and params["max_value"] is not None:
                template_str = f"Must have {at_least_str} $min_value and {at_most_str} $max_value rows."
            elif params["min_value"] is None:
                template_str = f"Must have {at_most_str} $max_value rows."
            elif params["max_value"] is None:
                template_str = f"Must have {at_least_str} $min_value rows."

        if params["row_condition"] is not None:
            (
                conditional_template_str,
                conditional_params,
            ) = parse_row_condition_string_pandas_engine(params["row_condition"])
            template_str = (
                conditional_template_str
                + ", then "
                + template_str[0].lower()
                + template_str[1:]
            )
            params.update(conditional_params)

        return [
            RenderedStringTemplateContent(
                **{
                    "content_block_type": "string_template",
                    "string_template": {
                        "template": template_str,
                        "params": params,
                        "styling": styling,
                    },
                }
            )
        ]

    def _validate(
        self,
        configuration: ExpectationConfiguration,
        metrics: Dict,
        runtime_configuration: dict = None,
        execution_engine: ExecutionEngine = None,
    ):
        return self._validate_metric_value_between(
            metric_name="table.row_count",
            configuration=configuration,
            metrics=metrics,
            runtime_configuration=runtime_configuration,
            execution_engine=execution_engine,
        )
