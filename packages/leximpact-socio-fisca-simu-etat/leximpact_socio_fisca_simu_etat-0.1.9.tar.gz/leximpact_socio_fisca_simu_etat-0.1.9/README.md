# French State Budget Simulation API




_HTTP API for OpenFisca_

Used by [LexImpact](https://leximpact.an.fr/), a simulator of the French tax-benefit system.

Make use of [OpenFisca](https://openfisca.org/en/) a rules as code tax benefit system.


## Install

`pip install leximpact_socio_fisca_simu_etat`

## How to use

Fill me in please! Don't forget code examples:

```python
from leximpact_socio_fisca_simu_etat.csg_simu import (
    ReformeSocioFiscale,
    compute_all_simulation,
)

reform = ReformeSocioFiscale(
    base=2021,
    amendement={
        "prelevements_sociaux.contributions_sociales.csg.activite.imposable.taux": 0.068,
    },
    output_variables=["csg"],
    quantile_nb=4,
    quantile_compare_variables=["csg"],
)
resultat = compute_all_simulation(reform, annee_de_calcul="2021")
```

    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:41] reform.amendement : None
    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:41] No cache for 5078a86c7201f132a44472774283e4a774e85b9bd94c88c9e756d3cb2021, compute it.
    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:45] OpenFisca a retourné des individus
    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:45] reform.amendement : {'prelevements_sociaux.contributions_sociales.csg.activite.imposable.taux': 0.068}
    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:45] No cache for 3580f21542881d1996a7b3a16a759d8318e58bdc44ac26ab6cfbf8662021, compute it.
    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:49] OpenFisca a retourné des individus
    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:49] Temps de traitement total pour la simulation 7.873102587996982 secondes


```python
print(
    f"Montant total de la csg : {resultat.result['amendement'].state_budget['csg']:,} €"
)
```

    Montant total de la csg : -147,054,542,277.62744 €


# How to develop

Please see contributing.
